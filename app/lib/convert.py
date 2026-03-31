from datetime import datetime
from typing import List, Optional, Tuple

import numpy as np
import pymap3d as pm
from pydantic import BaseModel

from app.models.a_to_be import (
    AbsoluteCoordinates,
    Dimensions,
    LocalCoordinates,
    ORTTrackingHistoryMessage,
    ORTTrackingRealtimeMessage,
    PathItem,
)
from app.models.common import TupleCoordinate
from app.models.outsight import Alert, OutsightMessage


class ReferencePlane(BaseModel):
    origin: TupleCoordinate
    point_on_positive_horizontal_axis: TupleCoordinate


class OutSightToAToBeConfig(BaseModel):
    outsight_reference_plane: ReferencePlane
    atobe_reference_plane: ReferencePlane


class OutSightToAToBe:
    def __init__(self, config: OutSightToAToBeConfig) -> None:
        self._config = config

        x, y, _ = pm.geodetic2enu(
            *config.outsight_reference_plane.origin,
            0,
            *config.atobe_reference_plane.origin,
            0,
        )
        local_outsight_origin = float(x), float(y)

        x, y, _ = pm.geodetic2enu(
            *config.outsight_reference_plane.point_on_positive_horizontal_axis,
            0,
            *config.atobe_reference_plane.origin,
            0,
        )
        local_outsight_hor_pos = float(x), float(y)

        x, y, _ = pm.geodetic2enu(
            *config.atobe_reference_plane.point_on_positive_horizontal_axis,
            0,
            *config.atobe_reference_plane.origin,
            0,
        )
        local_atobe_hor_pos = float(x), float(y)

        outsight_origin = np.array(local_outsight_origin)
        outsight_hor_pos = np.array(local_outsight_hor_pos)
        outsight_hor_vec = outsight_hor_pos - outsight_origin
        outsight_hor_vec /= np.linalg.norm(outsight_hor_vec)
        outsight_ver_vec = np.array((-outsight_hor_vec[1], outsight_hor_vec[0]))

        atobe_hor_vec = np.array(local_atobe_hor_pos)
        a, b = atobe_hor_vec / np.linalg.norm(atobe_hor_vec)

        self._outsight_to_enu_transformation_matrix = np.matrix(
            list(zip(outsight_hor_vec, outsight_ver_vec, outsight_origin))
        )

        enu_hor_vec = np.array((a, -b))
        enu_ver_vec = np.array((b, a))
        self._enu_to_atobe_transformation_matrix = np.matrix(
            list(zip(enu_hor_vec, enu_ver_vec))
        )

    def calculate_coords(
        self, data: Alert
    ) -> Tuple[LocalCoordinates, AbsoluteCoordinates]:
        outsight_point = np.array((*data.coordinate[3], 1))
        enu_point = np.matmul(
            self._outsight_to_enu_transformation_matrix, outsight_point
        ).A1
        lat, lon, _ = pm.enu2geodetic(
            enu_point[0],
            enu_point[1],
            0,
            self._config.atobe_reference_plane.origin[0],
            self._config.atobe_reference_plane.origin[1],
            0,
        )

        x, y = np.matmul(self._enu_to_atobe_transformation_matrix, enu_point).A1

        # x and y are flipped on purpose due to the atobe spec
        return LocalCoordinates(x=y, y=x), AbsoluteCoordinates(
            latitude=lat, longitude=lon
        )

    def calculate_dimensions(self, data: Alert) -> Dimensions:
        p0 = np.array(data.coordinate[0])
        p1 = np.array(data.coordinate[1])
        p2 = np.array(data.coordinate[2])
        p3 = np.array(data.coordinate[3])

        length0 = np.linalg.norm(p0 - p1)
        length1 = np.linalg.norm(p2 - p3)

        width0 = np.linalg.norm(p1 - p2)
        width1 = np.linalg.norm(p0 - p3)

        return Dimensions(
            length=float((length0 + length1) / 2),
            width=float((width0 + width1) / 2),
            height=data.height,
        )

    def _convert_alert(
        self, alert: Alert, timestamp: datetime
    ) -> ORTTrackingRealtimeMessage:
        local_coordinates, absolute_coordinates = self.calculate_coords(alert)
        dimensions = self.calculate_dimensions(alert)

        return ORTTrackingRealtimeMessage(
            objectID=alert.object_id,
            timeOfMeasurement=timestamp,
            speedKmh=alert.speed,
            absoluteCoordinates=absolute_coordinates,
            dimensions=dimensions,
            localCoordinates=local_coordinates,
        )

    def convert_outsight_to_ort_tracking_realtime_message(
        self, outsight_message: OutsightMessage
    ) -> ORTTrackingRealtimeMessage:

        alert = (
            outsight_message.data.out_alert
            if outsight_message.data.out_alert is not None
            else outsight_message.data.in_alert
        )

        timestamp = (
            outsight_message.end_timestamp
            if outsight_message.end_timestamp is not None
            else outsight_message.start_timestamp
        )

        return self._convert_alert(alert, timestamp)

    def convert_outsight_to_ort_tracking_history_message(
        self,
        msg: OutsightMessage,
    ) -> Optional[ORTTrackingHistoryMessage]:
        if msg.data.out_alert is None or msg.end_timestamp is None:
            return None

        path: List[PathItem] = []

        for alert, timestamp in (
            (msg.data.in_alert, msg.start_timestamp),
            (msg.data.out_alert, msg.end_timestamp),
        ):
            path.append(self._convert_alert(alert, timestamp))

        return ORTTrackingHistoryMessage(
            objectID=msg.data.in_alert.object_id,
            path=path,
        )
