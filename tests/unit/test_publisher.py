from __future__ import annotations

from unittest.mock import AsyncMock

from monitor.fetcher import NewsItem
from monitor.publisher import NewsPublisher


class TestNewsPublisher:
    async def test_publish_calls_broker(self, news_publisher: NewsPublisher):
        broker = news_publisher._broker
        broker.publish = AsyncMock()

        item = NewsItem(
            source="ria",
            title="Test",
            link="https://ria.ru/1",
            published_at="2024-01-01",
            text="Description",
        )

        await news_publisher.publish(item)

        broker.publish.assert_awaited_once_with(
            {
                "source": "ria",
                "title": "Test",
                "link": "https://ria.ru/1",
                "published_at": "2024-01-01",
                "text": "Description",
            },
            subject="news.rss",
        )

    async def test_publish_multiple_items(self, news_publisher: NewsPublisher):
        broker = news_publisher._broker
        broker.publish = AsyncMock()

        items = [
            NewsItem(
                source="ria",
                title=f"News {i}",
                link=f"https://ria.ru/{i}",
                published_at="",
                text="",
            )
            for i in range(3)
        ]

        for item in items:
            await news_publisher.publish(item)

        assert broker.publish.await_count == 3
