from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "CoffeeKing Backend"
    environment: str = "development"

    database_url: str = "sqlite:///./coffeeking.db"

    jwt_secret_key: str = "change-me-please-set-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
