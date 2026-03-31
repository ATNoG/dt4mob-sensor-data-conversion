from contextlib import asynccontextmanager
from typing import AsyncIterator, Self

from amqtt.client import QOS_0, ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig

from app.interfaces.consumer import ConsumerInterface
from app.settings.consumer import MQTTConsumerSettings


class MQTTConsumer(ConsumerInterface):
    """Reads all messages from subscribed topics and puts them to a queue."""

    def __init__(self, consumer_settings: MQTTConsumerSettings) -> None:
        self._settings = consumer_settings

        self._mqttc = MQTTClient(
            config=ClientConfig(
                connection=ConnectionConfig(uri=str(self._settings.url))
            )
        )

    async def _subscribe_all(self) -> None:
        await self._mqttc.subscribe((topic, QOS_0) for topic in self._settings.topics)

    @property
    @asynccontextmanager
    async def client(self) -> AsyncIterator[Self]:
        await self._mqttc.connect()

        await self._subscribe_all()

        yield self

        await self._mqttc.disconnect()

    @property
    async def messages(self) -> AsyncIterator[bytes]:
        while True:
            msg = await self._mqttc.deliver_message()
            if msg:
                yield bytes(msg.data)
