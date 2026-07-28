from __future__ import annotations

from unittest.mock import AsyncMock

import httpx
import pytest

from monitor.fetcher import RSSFetcher

RSS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <item>
    <title>News 1</title>
    <link>https://ria.ru/1</link>
    <description>Description 1</description>
    <pubDate>Mon, 01 Jan 2024 00:00:00 +0000</pubDate>
  </item>
  <item>
    <title>News 2</title>
    <link>https://ria.ru/2</link>
    <description>Description 2</description>
    <pubDate>Tue, 02 Jan 2024 00:00:00 +0000</pubDate>
  </item>
</channel>
</rss>"""

EMPTY_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
</channel>
</rss>"""


class TestRSSFetcher:
    async def test_fetch_returns_items(self, rss_fetcher: RSSFetcher, mocker):
        mock_response = AsyncMock()
        mock_response.text = RSS_XML
        mock_response.raise_for_status = mocker.Mock()

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        items = await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)

        assert len(items) == 2
        assert items[0].source == "ria"
        assert items[0].title == "News 1"
        assert items[0].link == "https://ria.ru/1"
        assert items[0].text == "Description 1"
        assert items[1].title == "News 2"

    async def test_deduplication(self, rss_fetcher: RSSFetcher, mocker):
        mock_response = AsyncMock()
        mock_response.text = RSS_XML
        mock_response.raise_for_status = mocker.Mock()

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        items_first = await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
        assert len(items_first) == 2

        items_second = await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
        assert len(items_second) == 0

    async def test_reset_seen(self, rss_fetcher: RSSFetcher, mocker):
        mock_response = AsyncMock()
        mock_response.text = RSS_XML
        mock_response.raise_for_status = mocker.Mock()

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
        rss_fetcher.reset_seen()

        items = await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
        assert len(items) == 2

    async def test_empty_rss(self, rss_fetcher: RSSFetcher, mocker):
        mock_response = AsyncMock()
        mock_response.text = EMPTY_RSS
        mock_response.raise_for_status = mocker.Mock()

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        items = await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
        assert len(items) == 0

    async def test_http_error(self, rss_fetcher: RSSFetcher, mocker):
        mock_response = mocker.MagicMock(spec=httpx.Response)
        mock_response.text = ""
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "404", request=mocker.Mock(), response=mocker.Mock()
        )

        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_client.get.return_value = mock_response

        with pytest.raises(httpx.HTTPStatusError):
            await rss_fetcher.fetch("ria", "https://ria.ru/rss", mock_client)
