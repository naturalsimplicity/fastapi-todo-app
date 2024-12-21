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

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
        }

settings = AppSettings()
