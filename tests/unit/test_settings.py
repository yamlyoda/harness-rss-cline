from __future__ import annotations

from monitor.settings import Settings as MonitorSettings
from worker.settings import Settings as WorkerSettings


class TestMonitorSettings:
    def test_default_values(self):
        s = MonitorSettings()
        assert s.nats_url == "nats://localhost:4222"
        assert s.monitor_interval_minutes == 5
        assert s.rss_sources == "ria,tass,kommersant"

    def test_rss_urls(self):
        s = MonitorSettings()
        urls = s.rss_urls
        assert "ria" in urls
        assert "tass" in urls
        assert "kommersant" in urls
        assert "https://ria.ru/export/rss2/archive/index.xml" in urls.values()

    def test_active_sources(self):
        s = MonitorSettings(rss_sources="ria,tass")
        assert s.active_sources == ["ria", "tass"]

    def test_active_sources_with_spaces(self):
        s = MonitorSettings(rss_sources="  ria , tass  ")
        assert s.active_sources == ["ria", "tass"]

    def test_active_sources_empty(self):
        s = MonitorSettings(rss_sources="")
        assert s.active_sources == []

    def test_active_sources_filters_empty(self):
        s = MonitorSettings(rss_sources="ria,,tass,")
        assert s.active_sources == ["ria", "tass"]


class TestWorkerSettings:
    def test_default_values(self):
        s = WorkerSettings()
        assert s.nats_url == "nats://localhost:4222"
        assert s.postgres_host == "localhost"
        assert s.postgres_port == 5432
        assert s.postgres_db == "rss_news"
        assert s.postgres_user == "rss_user"
        assert s.postgres_password == "rss_password"

    def test_postgres_dsn(self):
        s = WorkerSettings()
        dsn = s.postgres_dsn
        assert dsn.startswith("postgresql://")
        assert "rss_user" in dsn
        assert "rss_password" in dsn
        assert "localhost" in dsn
        assert "rss_news" in dsn

    def test_postgres_dsn_custom_values(self):
        s = WorkerSettings(
            postgres_host="pg.example.com",
            postgres_port=15432,
            postgres_db="custom_db",
            postgres_user="admin",
            postgres_password="secret",
        )
        assert (
            s.postgres_dsn == "postgresql://admin:secret@pg.example.com:15432/custom_db"
        )
