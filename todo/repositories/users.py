from aiosqlite import Connection

from todo.repositories.base import BaseRepository
from todo.database.queries import queries
from todo.database.errors import LoginIsUnavailable


class UsersRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        
    async def create_user(
        self,
        login: str,
        name: str
    ) -> int:
        if await queries.check_login_availability(
            self.connection,
            login=login
        ):
            raise LoginIsUnavailable(f"Login {login} is already used")
        
        user_id = await queries.create_new_user(
            self.connection,
            login=login,
            name=name
        )
        await self.connection.commit()
        return user_id