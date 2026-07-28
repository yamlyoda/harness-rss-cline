from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nats_url: str = "nats://localhost:4222"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "rss_news"
    postgres_user: str = "rss_user"
    postgres_password: str = "rss_password"

    @property
    def postgres_dsn(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
