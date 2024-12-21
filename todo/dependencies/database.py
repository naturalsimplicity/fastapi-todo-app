from typing import Annotated, AsyncGenerator, Callable, Type, Any
from aiosqlite import Connection, connect
from fastapi import Depends

from todo.core.settings import settings
from todo.repositories.base import BaseRepository


async def _get_connection() -> AsyncGenerator[Connection, Any]:
    async with connect(settings.database_url) as conn:
        yield conn

def get_repository(
    repo_type: Type[BaseRepository],
) -> Callable[[Connection], BaseRepository]:
    def _get_repo(
        conn: Annotated[Connection, Depends(_get_connection)],
    ) -> BaseRepository:
        return repo_type(conn)

    return _get_repo
