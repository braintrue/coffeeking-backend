"""Application configuration.

This module defines a Pydantic ``BaseSettings`` subclass that encapsulates all
environment variables used by the application.  Values will be read from
``.env`` if present.  See ``.env.example`` for a template.
"""

from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Centralised configuration values for the application."""

    app_name: str = "CoffeeKing Backend"
    environment: str = "development"
    database_url: str = "sqlite:///./coffeeking.db"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return a cached instance of Settings.

    Using ``lru_cache`` ensures that settings are only parsed once per
    interpreter instance.
    """
    return Settings()