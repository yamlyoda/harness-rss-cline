from __future__ import annotations

from collections.abc import AsyncGenerator

import asyncpg
import pytest_asyncio
from faststream.nats import NatsBroker

from worker.db import Database

TEST_NATS_URL = "nats://localhost:4223"
TEST_PG_HOST = "localhost"
TEST_PG_PORT = 5433
TEST_PG_DB = "rss_news_test"
TEST_PG_USER = "test_user"
TEST_PG_PASS = "test_pass"


@pytest_asyncio.fixture(scope="session")
async def nats_broker() -> AsyncGenerator[NatsBroker, None]:
    broker = NatsBroker(TEST_NATS_URL)
    await broker.connect()
    yield broker
    await broker.close()


@pytest_asyncio.fixture(scope="session")
async def database() -> AsyncGenerator[Database, None]:
    db = Database()
    db._pool = await _create_pool()  # type: ignore[assignment]
    yield db
    await db._pool.close()


async def _create_pool():
    return await asyncpg.create_pool(
        host=TEST_PG_HOST,
        port=TEST_PG_PORT,
        database=TEST_PG_DB,
        user=TEST_PG_USER,
        password=TEST_PG_PASS,
    )


@pytest_asyncio.fixture(autouse=True)
async def cleanup_db(database: Database) -> AsyncGenerator[None, None]:
    yield
    async with database._pool.acquire() as conn:
        await conn.execute("DELETE FROM entities")
        await conn.execute("DELETE FROM news")
