from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nats_url: str = "nats://localhost:4222"
    monitor_interval_minutes: int = 5
    rss_sources: str = "ria,tass,kommersant"
    rss_url_ria: str = "https://ria.ru/export/rss2/archive/index.xml"
    rss_url_tass: str = "https://tass.ru/rss/v2.xml"
    rss_url_kommersant: str = "https://www.kommersant.ru/RSS/news.xml"

    @property
    def rss_urls(self) -> dict[str, str]:
        return {
            "ria": self.rss_url_ria,
            "tass": self.rss_url_tass,
            "kommersant": self.rss_url_kommersant,
        }

    @property
    def active_sources(self) -> list[str]:
        return [s.strip() for s in self.rss_sources.split(",") if s.strip()]


settings = Settings()
