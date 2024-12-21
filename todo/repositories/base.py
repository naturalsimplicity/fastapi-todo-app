from aiosqlite import Connection


class BaseRepository:
    def __init__(self, connection: Connection) -> None:
        self._connection = connection

    @property
    def connection(self) -> Connection:
        return self._connection
