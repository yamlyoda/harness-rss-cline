from __future__ import annotations

import asyncio
import logging

from faststream.nats import NatsBroker

from worker.db import Database
from worker.handler import NewsHandler, NewsMessage
from worker.ner import NERExtractor
from worker.settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> None:
    db = Database()
    await db.connect()

    ner = NERExtractor()
    handler = NewsHandler(db, ner)

    broker = NatsBroker(settings.nats_url)

    @broker.subscriber("news.rss")
    async def on_news(msg: NewsMessage) -> None:
        await handler.handle(msg)

    async with broker:
        await broker.start()
        logger.info("Worker started, waiting for messages...")
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            pass
        finally:
            await db.close()


if __name__ == "__main__":
    asyncio.run(main())
