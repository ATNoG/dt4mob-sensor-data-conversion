from enum import StrEnum
from typing import Annotated, List, Literal

from pydantic import AnyUrl, BaseModel, Field

from app.models.common import NonEmptyStr, Port


class ConsumerBackend(StrEnum):
    MQTT = "mqtt"
    WEBHOOK = "webhook"
    DISABLED = "disabled"


class BaseConsumerSettings(BaseModel):
    pass


class DisabledConsumerSettings(BaseConsumerSettings):
    backend: Literal[ConsumerBackend.DISABLED] = ConsumerBackend.DISABLED


class MQTTConsumerSettings(BaseConsumerSettings):
    backend: Literal[ConsumerBackend.MQTT] = ConsumerBackend.MQTT
    url: AnyUrl = AnyUrl("mqtt://localhost")

    topics: List[str] = []


class WebhookConsumerSettings(BaseConsumerSettings):
    backend: Literal[ConsumerBackend.WEBHOOK] = ConsumerBackend.WEBHOOK
    host: NonEmptyStr = "localhost"
    port: Port = 8000

    base_path: str = "/"


type ConsumerSettings = Annotated[
    MQTTConsumerSettings | WebhookConsumerSettings | DisabledConsumerSettings,
    Field(discriminator="backend"),
]
