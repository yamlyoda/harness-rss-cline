from __future__ import annotations

from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from faststream.nats import NatsBroker

from monitor.fetcher import RSSFetcher
from monitor.publisher import NewsPublisher
from monitor.settings import settings


class MonitorService:
    def __init__(self) -> None:
        self.fetcher = RSSFetcher()
        self.broker = NatsBroker(settings.nats_url)
        self.publisher = NewsPublisher(self.broker)

    async def poll_all(self) -> int:
        total = 0
        async with httpx.AsyncClient() as client:
            for source in settings.active_sources:
                url = settings.rss_urls.get(source)
                if not url:
                    continue
                items = await self.fetcher.fetch(source, url, client)
                for item in items:
                    await self.publisher.publish(item)
                total += len(items)
        return total


service = MonitorService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await service.broker.connect()
    yield
    await service.broker.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/refresh")
async def refresh():
    count = await service.poll_all()
    return {"new_items": count}
