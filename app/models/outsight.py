from datetime import datetime
from typing import Optional, Tuple

from pydantic import BaseModel, ConfigDict, NonNegativeFloat

type Coord = Tuple[float, float]  # Not geographical coordinates
type BoundingSquare = Tuple[Coord, Coord, Coord, Coord]


class Alert(BaseModel):
    model_config = ConfigDict(extra="allow")
    object_id: int
    speed: NonNegativeFloat
    coordinate: BoundingSquare
    height: NonNegativeFloat


class Data(BaseModel):
    in_alert: Alert
    out_alert: Optional[Alert]


class OutsightMessage(BaseModel):
    start_timestamp: datetime
    end_timestamp: Optional[datetime]
    data: Data
