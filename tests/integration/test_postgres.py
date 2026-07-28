from __future__ import annotations

import pytest

from worker.db import Database


@pytest.mark.integration
class TestPostgres:
    async def test_insert_news_and_read(self, database: Database):
        news_id = await database.insert_news(
            source="ria",
            title="Test News",
            link="https://ria.ru/test1",
            published_at="2024-01-01 12:00:00",
            text="Test description",
        )

        assert news_id > 0

        async with database._pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM news WHERE id = $1", news_id)

        assert row is not None
        assert row["source"] == "ria"
        assert row["title"] == "Test News"
        assert row["link"] == "https://ria.ru/test1"
        assert row["text"] == "Test description"

    async def test_insert_duplicate_link(self, database: Database):
        news_id_1 = await database.insert_news(
            source="ria",
            title="First",
            link="https://ria.ru/dup",
            published_at="",
            text="",
        )
        news_id_2 = await database.insert_news(
            source="tass",
            title="Second",
            link="https://ria.ru/dup",
            published_at="",
            text="",
        )

        assert news_id_1 > 0
        assert news_id_2 == 0

    async def test_insert_entities(self, database: Database):
        news_id = await database.insert_news(
            source="ria",
            title="Entity Test",
            link="https://ria.ru/entities",
            published_at="",
            text="About Москва and Путин",
        )

        entities = [
            {"text": "Москва", "label": "LOC", "count": 1},
            {"text": "Путин", "label": "PER", "count": 1},
        ]

        await database.insert_entities(news_id, entities)

        async with database._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM entities WHERE news_id = $1 ORDER BY id",
                news_id,
            )

        assert len(rows) == 2
        assert rows[0]["text"] == "Москва"
        assert rows[0]["label"] == "LOC"
        assert rows[1]["text"] == "Путин"
        assert rows[1]["label"] == "PER"

    async def test_cascade_delete(self, database: Database):
        news_id = await database.insert_news(
            source="ria",
            title="Cascade Test",
            link="https://ria.ru/cascade",
            published_at="",
            text="Test",
        )

        await database.insert_entities(
            news_id, [{"text": "Test", "label": "LOC", "count": 1}]
        )

        async with database._pool.acquire() as conn:
            await conn.execute("DELETE FROM news WHERE id = $1", news_id)

        async with database._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM entities WHERE news_id = $1", news_id
            )

        assert len(rows) == 0
