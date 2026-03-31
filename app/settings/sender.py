from pydantic import AnyUrl, BaseModel


class SenderSettings(BaseModel):
    url: AnyUrl = AnyUrl("mqtt://localhost")
