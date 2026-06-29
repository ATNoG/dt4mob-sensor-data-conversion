import asyncio
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import AsyncIterator, Self

import uvicorn
from fastapi import FastAPI, Request

from app.interfaces.consumer import ConsumerInterface
from app.settings.consumer import WebhookConsumerSettings


class WebhookConsumer(ConsumerInterface):
    def __init__(self, consumer_settings: WebhookConsumerSettings) -> None:
        self.settings = consumer_settings
        self.queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.app = FastAPI()

        @self.app.post(consumer_settings.base_path, status_code=HTTPStatus.NO_CONTENT)
        async def _(request: Request) -> None:
            body = await request.body()
            await self.queue.put(body)

    @property
    @asynccontextmanager
    async def client(self) -> AsyncIterator[Self]:
        config = uvicorn.Config(
            app=self.app, host=self.settings.host, port=self.settings.port
        )
        server = uvicorn.Server(config)

        task = asyncio.create_task(server.serve())

        yield self

        task.cancel()

    @property
    async def messages(self) -> AsyncIterator[bytes]:
        while True:
            yield await self.queue.get()
