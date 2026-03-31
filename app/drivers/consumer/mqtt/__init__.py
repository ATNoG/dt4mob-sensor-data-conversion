from app.drivers.consumer.mqtt.consumer import MQTTConsumer
from app.settings import settings
from app.settings.consumer import ConsumerBackend

if settings.consumer.backend != ConsumerBackend.MQTT:
    raise RuntimeError("MQTT Consumer instantiated but backend isn't MQTT")

mqtt_consumer = MQTTConsumer(settings.consumer)
