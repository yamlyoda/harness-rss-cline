from __future__ import annotations

from monitor.fetcher import NewsItem


class TestNewsItem:
    def test_guid_consistency(self):
        item1 = NewsItem(
            source="ria",
            title="Test News",
            link="https://ria.ru/test1",
            published_at="2024-01-01",
            text="Some text",
        )
        item2 = NewsItem(
            source="ria",
            title="Test News",
            link="https://ria.ru/test1",
            published_at="2024-01-01",
            text="Some text",
        )
        assert item1.guid == item2.guid

    def test_guid_different_for_different_news(self):
        item1 = NewsItem(
            source="ria",
            title="News A",
            link="https://ria.ru/a",
            published_at="2024-01-01",
            text="Text A",
        )
        item2 = NewsItem(
            source="tass",
            title="News B",
            link="https://tass.ru/b",
            published_at="2024-01-02",
            text="Text B",
        )
        assert item1.guid != item2.guid

    def test_guid_different_source_same_title(self):
        item1 = NewsItem(
            source="ria",
            title="Same Title",
            link="https://ria.ru/1",
            published_at="",
            text="",
        )
        item2 = NewsItem(
            source="tass",
            title="Same Title",
            link="https://tass.ru/1",
            published_at="",
            text="",
        )
        assert item1.guid != item2.guid

    def test_fields(self):
        item = NewsItem(
            source="ria",
            title="Title",
            link="https://ria.ru/1",
            published_at="2024-01-01",
            text="Description",
        )
        assert item.source == "ria"
        assert item.title == "Title"
        assert item.link == "https://ria.ru/1"
        assert item.published_at == "2024-01-01"
        assert item.text == "Description"
