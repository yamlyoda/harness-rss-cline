from __future__ import annotations

import asyncpg

from worker.settings import settings


class Database:
    def __init__(self) -> None:
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        self._pool = await asyncpg.create_pool(
            host=settings.postgres_host,
            port=settings.postgres_port,
            database=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
        )

    async def close(self) -> None:
        if self._pool:
            await self._pool.close()

    async def insert_news(
        self,
        source: str,
        title: str,
        link: str,
        published_at: str,
        text: str,
    ) -> int:
        async with self._pool.acquire() as conn:  # type: ignore[union-attr]
            row = await conn.fetchrow(
                """
                INSERT INTO news (source, title, link, published_at, text)
                VALUES ($1, $2, $3, NULLIF($4, '')::TIMESTAMP, $5)
                ON CONFLICT (link) DO NOTHING
                RETURNING id
                """,
                source,
                title,
                link,
                published_at,
                text,
            )
            return row["id"] if row else 0

    async def insert_entities(self, news_id: int, entities: list[dict]) -> None:
        async with self._pool.acquire() as conn:  # type: ignore[union-attr]
            for ent in entities:
                await conn.execute(
                    """
                    INSERT INTO entities (news_id, text, label, count)
                    VALUES ($1, $2, $3, $4)
                    """,
                    news_id,
                    ent["text"],
                    ent["label"],
                    ent["count"],
                )
