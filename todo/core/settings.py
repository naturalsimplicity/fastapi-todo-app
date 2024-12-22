from pydantic_settings import BaseSettings
from typing import Any
import logging


class AppSettings(BaseSettings):
    debug: bool = False
    title: str = "FastAPI ToDo application"
    version: str = "0.0.1"

    api_prefix: str = "/api"

    logging_level: int = logging.DEBUG
    database_url: str = "sqlite:///../database.db"

    secret_key: str = "very-secret-key"
    encryption_algorithm: str = 'HS256'
    access_token_expire_seconds: int = 60 * 60 * 24  # one day

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

settings = AppSettings()

def get_app_settings() -> AppSettings:
    return settings
