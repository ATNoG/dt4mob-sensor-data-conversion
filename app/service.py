import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional, Tuple

from loguru import logger
from pydantic import ValidationError

from app.drivers.consumer import get_consumer
from app.interfaces.consumer import ConsumerInterface
from app.lib.convert import OutSightToAToBe
from app.models.outsight import OutsightMessage
from app.sender import Sender
from app.settings import settings


class Service:
    def __init__(self) -> None:
        self._consumer = get_consumer()
        self._sender = Sender(settings.sender)
        self._converter = OutSightToAToBe(settings.converter)

    @property
    @asynccontextmanager
    async def _resoures(self) -> AsyncIterator[Tuple[ConsumerInterface, Sender]]:
        async with self._consumer.client as consumer, self._sender.client as sender:
            yield consumer, sender

    def _convert(self, msg: bytes) -> Tuple[bytes, Optional[bytes]]:
        outsight = OutsightMessage.model_validate_json(msg)

        atb_hist = self._converter.convert_outsight_to_ort_tracking_history_message(
            outsight
        )
        return (
            self._converter.convert_outsight_to_ort_tracking_realtime_message(outsight)
            .model_dump_json(exclude_none=True)
            .encode()
        ), (
            atb_hist
            if atb_hist is None
            else atb_hist.model_dump_json(exclude_none=True).encode()
        )

    async def run(self) -> None:
        async with self._resoures as (consumer, sender):
            logger.info("Service started successfully")
            try:
                async for msg in consumer.messages:
                    logger.debug("Received message: {}", msg)
                    try:
                        atb_msg, atb_hist_msg = self._convert(msg)
                    except ValidationError as e:
                        logger.warning(
                            "Received message was not a valid OutSight message: {}", e
                        )
                        continue
                    await sender.send(settings.atb_realtime_topic, atb_msg)
                    if atb_hist_msg:
                        await sender.send(settings.atb_history_topic, atb_hist_msg)
                    logger.debug("Sending message: {}", atb_msg)
            except (KeyboardInterrupt, asyncio.CancelledError):
                logger.info("Service terminating...")
