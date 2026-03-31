from typing import Optional

from app.interfaces.consumer import ConsumerInterface
from app.settings import settings
from app.settings.consumer import ConsumerBackend

consumer: Optional[ConsumerInterface] = None
match settings.consumer.backend:
    case ConsumerBackend.MQTT:
        from .mqtt import mqtt_consumer

        consumer = mqtt_consumer

    case ConsumerBackend.WEBHOOK:
        from .webhook import webhook_consumer

        consumer = webhook_consumer


def get_consumer() -> ConsumerInterface:
    if consumer is None:
        raise RuntimeError(
            "Disabled consumer is not supported, please provide a valid consumer"
        )
    return consumer
