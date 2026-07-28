from __future__ import annotations

import logging

from pydantic import BaseModel

from worker.db import Database
from worker.ner import NERExtractor

logger = logging.getLogger(__name__)


class NewsMessage(BaseModel):
    source: str
    title: str
    link: str
    published_at: str
    text: str


class NewsHandler:
    def __init__(self, db: Database, ner: NERExtractor) -> None:
        self._db = db
        self._ner = ner

    async def handle(self, msg: NewsMessage) -> None:
        try:
            news_id = await self._db.insert_news(
                source=msg.source,
                title=msg.title,
                link=msg.link,
                published_at=msg.published_at,
                text=msg.text,
            )
            if not news_id:
                logger.info("Duplicate skipped: %s", msg.link)
                return

            combined = f"{msg.title}\n{msg.text}"
            entities = self._ner.extract(combined)
            if entities:
                await self._db.insert_entities(news_id, entities)

            logger.info(
                "Processed news #%d from %s: %d entities",
                news_id,
                msg.source,
                len(entities),
            )
        except Exception:
            logger.exception("Failed to process message: %s", msg.link)
