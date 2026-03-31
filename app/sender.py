from contextlib import asynccontextmanager
from typing import AsyncGenerator, Self

from amqtt.client import ClientConfig, MQTTClient
from amqtt.contexts import ConnectionConfig

from app.settings.sender import SenderSettings


class Sender:
    def __init__(self, sender_settings: SenderSettings) -> None:
        self._settings = sender_settings

        self._mqttc = MQTTClient(
            config=ClientConfig(
                reconnect_retries=-1,
                connection=ConnectionConfig(uri=str(self._settings.url)),
            )
        )

    @property
    @asynccontextmanager
    async def client(self) -> AsyncGenerator[Self, None]:
        await self._mqttc.connect()

        yield self

        await self._mqttc.disconnect()

    async def send(self, topic: str, payload: bytes) -> None:
        await self._mqttc.publish(topic, payload)
