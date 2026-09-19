"""Вложенные секции читаются через двойное подчёркивание: POSTGRES__HOST, POSTGRES__PORT."""

from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    host: str = "postgres"
    port: int = 5432
    user: str = "app_user"
    password: str = "supersecretpassword"
    db: str = "postgres"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    domain: str = "localhost"
    secure: bool = False
    # Префикс, под которым Traefik отдаёт бэкенд (PathPrefix(`/api`)). Traefik
    # префикс не срезает, поэтому роуты монтируются именно под ним.
    api_prefix: str = "/api"

    postgres: PostgresSettings = PostgresSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
