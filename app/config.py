from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
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
    return Settings()
