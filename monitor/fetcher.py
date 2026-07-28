from __future__ import annotations

import hashlib
from dataclasses import dataclass

import feedparser
import httpx


@dataclass
class NewsItem:
    source: str
    title: str
    link: str
    published_at: str
    text: str

    @property
    def guid(self) -> str:
        return hashlib.sha256(
            (self.source + self.title + self.link).encode()
        ).hexdigest()


class RSSFetcher:
    def __init__(self, seen_guids: set[str] | None = None) -> None:
        self._seen: set[str] = seen_guids or set()

    async def fetch(
        self, source: str, url: str, client: httpx.AsyncClient
    ) -> list[NewsItem]:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()

        feed = feedparser.parse(response.text)
        items: list[NewsItem] = []

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            text = entry.get("description", "")
            published = entry.get("published", "")

            item = NewsItem(
                source=source,
                title=title,
                link=link,
                published_at=published,
                text=text,
            )

            if item.guid not in self._seen:
                self._seen.add(item.guid)
                items.append(item)

        return items

    def reset_seen(self) -> None:
        self._seen.clear()
