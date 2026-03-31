from app.drivers.consumer.webhook.consumer import WebhooConsumer
from app.settings import settings
from app.settings.consumer import ConsumerBackend

if settings.consumer.backend != ConsumerBackend.WEBHOOK:
    raise RuntimeError("Webhook Consumer instantiated but backend isn't webhook")

webhook_consumer = WebhooConsumer(settings.consumer)
