from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

from worker.db import Database


class TestDatabase:
    async def test_connect_creates_pool(self, mocker):
        mock_pool = AsyncMock()
        mock_create = AsyncMock(return_value=mock_pool)
        mocker.patch("asyncpg.create_pool", mock_create)

        db = Database()
        await db.connect()

        assert db._pool is mock_pool

    async def test_close_releases_pool(self, mocker):
        mock_pool = AsyncMock()
        mock_create = AsyncMock(return_value=mock_pool)
        mocker.patch("asyncpg.create_pool", mock_create)

        db = Database()
        await db.connect()
        await db.close()

        mock_pool.close.assert_awaited_once()

    async def test_close_without_connect(self):
        db = Database()
        await db.close()

    async def _setup_mock_pool(self, mocker):
        mock_conn = AsyncMock()
        mock_pool = MagicMock()
        mock_pool.acquire.return_value.__aenter__.return_value = mock_conn
        mock_create = AsyncMock(return_value=mock_pool)
        mocker.patch("asyncpg.create_pool", mock_create)
        db = Database()
        await db.connect()
        return db, mock_pool, mock_conn

    async def test_insert_news_returns_id(self, mocker):
        db, _mock_pool, mock_conn = await self._setup_mock_pool(mocker)
        mock_conn.fetchrow.return_value = {"id": 42}

        news_id = await db.insert_news(
            source="ria",
            title="Test",
            link="https://ria.ru/1",
            published_at="2024-01-01",
            text="Description",
        )

        assert news_id == 42
        mock_conn.fetchrow.assert_called_once()

    async def test_insert_news_duplicate_returns_zero(self, mocker):
        db, _mock_pool, mock_conn = await self._setup_mock_pool(mocker)
        mock_conn.fetchrow.return_value = None

        news_id = await db.insert_news(
            source="ria",
            title="Duplicate",
            link="https://ria.ru/dup",
            published_at="",
            text="",
        )

        assert news_id == 0

    async def test_insert_entities(self, mocker):
        db, _mock_pool, mock_conn = await self._setup_mock_pool(mocker)

        entities = [
            {"text": "Москва", "label": "LOC", "count": 1},
            {"text": "Путин", "label": "PER", "count": 2},
        ]

        await db.insert_entities(42, entities)

        assert mock_conn.execute.await_count == 2

    async def test_insert_entities_empty_list(self, mocker):
        db, _mock_pool, mock_conn = await self._setup_mock_pool(mocker)

        await db.insert_entities(42, [])

        mock_conn.execute.assert_not_awaited()
