from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from worker.handler import NewsHandler, NewsMessage


class TestNewsHandler:
    async def test_handle_success(self, news_handler: NewsHandler):
        msg = NewsMessage(
            source="ria",
            title="Test News",
            link="https://ria.ru/1",
            published_at="2024-01-01",
            text="Some text about Москва",
        )

        news_handler._db.insert_news = AsyncMock(return_value=42)
        news_handler._ner.extract = MagicMock(
            return_value=[{"text": "Москва", "label": "LOC", "count": 1}]
        )
        news_handler._db.insert_entities = AsyncMock()

        await news_handler.handle(msg)

        news_handler._db.insert_news.assert_awaited_once_with(
            source="ria",
            title="Test News",
            link="https://ria.ru/1",
            published_at="2024-01-01",
            text="Some text about Москва",
        )
        news_handler._ner.extract.assert_called_once_with(
            "Test News\nSome text about Москва"
        )
        news_handler._db.insert_entities.assert_awaited_once_with(
            42, [{"text": "Москва", "label": "LOC", "count": 1}]
        )

    async def test_handle_duplicate(self, news_handler: NewsHandler):
        msg = NewsMessage(
            source="ria",
            title="Duplicate",
            link="https://ria.ru/dup",
            published_at="",
            text="",
        )

        news_handler._db.insert_news = AsyncMock(return_value=0)
        news_handler._db.insert_entities = AsyncMock()
        news_handler._ner.extract = MagicMock()

        await news_handler.handle(msg)

        news_handler._db.insert_news.assert_awaited_once()
        news_handler._ner.extract.assert_not_called()
        news_handler._db.insert_entities.assert_not_called()

    async def test_handle_no_entities(self, news_handler: NewsHandler):
        msg = NewsMessage(
            source="ria",
            title="Plain News",
            link="https://ria.ru/plain",
            published_at="",
            text="Just text without entities",
        )

        news_handler._db.insert_news = AsyncMock(return_value=10)
        news_handler._db.insert_entities = AsyncMock()
        news_handler._ner.extract = MagicMock(return_value=[])

        await news_handler.handle(msg)

        news_handler._ner.extract.assert_called_once()
        news_handler._db.insert_entities.assert_not_called()

    async def test_handle_error_logged(self, news_handler: NewsHandler, caplog):
        msg = NewsMessage(
            source="ria",
            title="Error Test",
            link="https://ria.ru/error",
            published_at="",
            text="",
        )

        news_handler._db.insert_news = AsyncMock(side_effect=Exception("DB error"))

        await news_handler.handle(msg)

        assert "Failed to process message" in caplog.text
        assert "https://ria.ru/error" in caplog.text
