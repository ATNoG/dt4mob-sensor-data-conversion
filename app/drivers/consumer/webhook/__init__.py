from app.drivers.consumer.webhook.consumer import WebhookConsumer
from app.settings import settings
from app.settings.consumer import ConsumerBackend

if settings.consumer.backend != ConsumerBackend.WEBHOOK:
    raise RuntimeError("Webhook Consumer instantiated but backend isn't webhook")

webhook_consumer = WebhookConsumer(settings.consumer)
