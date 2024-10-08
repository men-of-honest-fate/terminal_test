import os
from functools import lru_cache

from pydantic import ConfigDict, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    DB_DSN: str = os.getenv(
        "DB_DSN", "postgresql://postgres:12345@localhost:5432/terminals"
    )
    ROOT_PATH: str = os.getenv("APP_NAME", "")
    API_URL: str = os.getenv("API_URL", "localhost:8000")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    COM: str = os.getenv("COM", "COM4")
    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    model_config = ConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
