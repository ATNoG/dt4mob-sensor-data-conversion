from enum import StrEnum
from typing import Annotated, Optional, Self

from pydantic import AwareDatetime, BaseModel, Field

from app.models.common import Lat, Lon

Timestamp = AwareDatetime


class ORTTrackingMessageBase(BaseModel):
    objectID: int
    triggeringTimestamp: Optional[Timestamp] = None


class CoordinateReference(StrEnum):
    right_rear_bottom_corner = "right_rear_bottom_corner"
    right_front_bottom_corner = "right_front_bottom_corner"


class LocalCoordinates(BaseModel):
    x: float
    y: float


class AbsoluteCoordinates(BaseModel):
    latitude: float
    longitude: float

    @classmethod
    def from_tuple(cls, lat: Lat, lon: Lon) -> Self:
        return cls(latitude=lat, longitude=lon)


class Dimensions(BaseModel):
    width: Optional[float] = None
    length: Optional[float] = None
    height: Optional[float] = None


class PathItem(BaseModel):
    timeOfMeasurement: Timestamp
    speedKmh: Optional[float] = None
    coordinatesReference: Optional[CoordinateReference] = (
        CoordinateReference.right_rear_bottom_corner
    )
    localCoordinates: LocalCoordinates
    absoluteCoordinates: AbsoluteCoordinates
    dimensions: Dimensions


class ORTTrackingHistoryMessage(ORTTrackingMessageBase):
    path: Annotated[list[PathItem], Field(min_length=1)]


class ORTTrackingRealtimeMessage(ORTTrackingMessageBase, PathItem):
    pass
