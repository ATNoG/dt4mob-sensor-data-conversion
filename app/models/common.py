from typing import Annotated

from pydantic import Field

type Lon = Annotated[float, Field(ge=-180, le=180)]
type Lat = Annotated[float, Field(ge=-90, le=90)]

type TupleCoordinate = tuple[Lat, Lon]

type NonEmptyStr = Annotated[str, Field(min_length=1, description="Not empty string")]
type Port = Annotated[int, Field(ge=0, le=65535, description="A valid port number")]
