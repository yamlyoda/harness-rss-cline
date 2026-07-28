from __future__ import annotations

from faststream.nats import NatsBroker

from monitor.fetcher import NewsItem


class NewsPublisher:
    def __init__(self, broker: NatsBroker) -> None:
        self._broker = broker

    async def publish(self, item: NewsItem) -> None:
        await self._broker.publish(
            {
                "source": item.source,
                "title": item.title,
                "link": item.link,
                "published_at": item.published_at,
                "text": item.text,
            },
            subject="news.rss",
        )
