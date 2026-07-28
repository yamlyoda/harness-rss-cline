from __future__ import annotations

from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from faststream.nats import NatsBroker

from monitor.fetcher import RSSFetcher
from monitor.publisher import NewsPublisher
from monitor.settings import settings as monitor_settings
from worker.db import Database
from worker.handler import NewsHandler
from worker.ner import NERExtractor


@pytest.fixture
def rss_fetcher() -> RSSFetcher:
    return RSSFetcher()


@pytest.fixture
def nats_broker() -> NatsBroker:
    return NatsBroker(monitor_settings.nats_url)


@pytest.fixture
def news_publisher(nats_broker: NatsBroker) -> NewsPublisher:
    return NewsPublisher(nats_broker)


@pytest.fixture
def ner_extractor(mocker):
    mock_nlp = mocker.MagicMock()
    mocker.patch("spacy.load", return_value=mock_nlp)
    return NERExtractor()


@pytest.fixture
def db() -> Database:
    return Database()


@pytest.fixture
def news_handler(db: Database, ner_extractor: NERExtractor) -> NewsHandler:
    return NewsHandler(db, ner_extractor)


# Integration fixtures


@pytest_asyncio.fixture(scope="session")
async def real_nats_broker() -> AsyncGenerator[NatsBroker, None]:
    broker = NatsBroker("nats://localhost:4223")
    await broker.connect()
    yield broker
    await broker.close()


@pytest_asyncio.fixture(scope="session")
async def real_db() -> AsyncGenerator[Database, None]:
    db = Database()
    await db.connect()
    yield db
    await db.close()
