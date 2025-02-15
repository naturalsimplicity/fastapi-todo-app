from pydantic_settings import BaseSettings
from typing import Any
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import pathlib
from aiosqlite import connect

from todo.database.queries import queries


class AppSettings(BaseSettings):
    debug: bool = False
    title: str = "FastAPI ToDo application"
    version: str = "0.0.1"

    api_prefix: str = "/api"

    logging_level: int = logging.DEBUG
    database_path: str = "database.db"

    secret_key: str = "very-secret-key"
    encryption_algorithm: str = 'HS256'
    access_token_expire_seconds: int = 60 * 60 * 24  # one day

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        if not pathlib.Path(self.database_path).exists():
            async with connect(f"{self.database_path}") as conn:
                await queries.create_table_users(conn)
                await queries.create_table_items(conn)
        yield

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
            "lifespan": self.lifespan
        }

settings = AppSettings()

def get_app_settings() -> AppSettings:
    return settings
