from aiosqlite import Connection

from todo.repositories.base import BaseRepository
from todo.models.domain.items import Item
from todo.database.queries import queries
from todo.database.errors import ItemDoesNotExist


class ItemsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    async def create_item(
        self,
        user_id: int,
        title: str,
        description: str,
        completed: bool
    ) -> int:
        item_id = await queries.create_new_item(
            self.connection,
            user_id=user_id,
            title=title,
            description=description,
            completed=completed
        )
        await self.connection.commit()
        return item_id

    async def get_item(
        self,
        item_id: int
    ) -> Item:
        if not await queries.check_if_item_exists(
            item_id=item_id
        ):
            raise ItemDoesNotExist
        return await queries.get_item(
            self.connection,
            item_id
        )

    async def get_all_items(self) -> list[Item]:
        return await queries.get_all_items(self.connection)

    async def get_user_items(self, user_id: int) -> list[Item]:
        return await queries.get_user_items(self.connection, user_id=user_id)
    
    async def update_item(
        self,
        item_id: int,
        title: str,
        desciption: str,
        completed: bool
    ) -> None:
        if not await queries.check_if_item_exists(
            item_id=item_id
        ):
            raise ItemDoesNotExist
        await queries.update_item(
            self.connection,
            item_id=item_id,
            title=title,
            desciption=desciption,
            completed=completed
        )

    async def delete_item(
        self,
        item_id: int
    ) -> None:
        if not await queries.check_if_item_exists(
            item_id=item_id
        ):
            raise ItemDoesNotExist
        await queries.delete_item(
            self.connection,
            item_id=item_id
        )