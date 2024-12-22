from aiosqlite import Connection

from todo.services.base import BaseService
from todo.models.items import ItemID, Item
from todo.database.queries import queries
from todo.exceptions import NoEnoughPriviligesError, ItemDoesNotExistError


class ItemService(BaseService):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    async def create_item(
        self,
        user_id: int,
        title: str,
        description: str,
        completed: bool
    ) -> ItemID:
        item_id = await queries.create_new_item(
            self.connection,
            user_id=user_id,
            title=title,
            description=description,
            completed=completed
        )
        await self.connection.commit()
        return ItemID(
            id=item_id
        )

    async def get_item(
        self,
        item_id: int
    ) -> Item:
        if not await queries.check_if_item_exists(
            self.connection,
            item_id=item_id
        ):
            raise ItemDoesNotExistError
        id_, user_id, title, description, completed = await queries.get_item(
            self.connection,
            item_id=item_id
        )
        return Item(
            id=id_,
            user_id=user_id,
            title=title,
            description=description,
            completed=completed
        )

    async def get_items(self, login: str = None) -> list[Item]:
        if login is None:
            items = await queries.get_all_items(self.connection)
        else:
            items = await queries.get_user_items(self.connection, login=login)
        return [
            Item(
                id=id_,
                user_id=user_id,
                title=title,
                description=description,
                completed=completed
            )
            for id_, user_id, title, description, completed in items
        ]
    
    async def update_item(
        self,
        user_id: int,
        item_id: int,
        title: str,
        description: str,
        completed: bool
    ) -> None:
        if not await queries.check_if_item_exists(
            self.connection,
            item_id=item_id
        ):
            raise ItemDoesNotExistError
        
        item_creator = await queries.get_item_creator(
            self.connection,
            item_id=item_id
        )
        if item_creator != user_id:
            raise NoEnoughPriviligesError

        await queries.update_item(
            self.connection,
            item_id=item_id,
            user_id=user_id,
            title=title,
            description=description,
            completed=completed
        )
        await self.connection.commit()

    async def delete_item(
        self,
        item_id: int,
        user_id: int
    ) -> None:
        if not await queries.check_if_item_exists(
            self.connection,
            item_id=item_id
        ):
            raise ItemDoesNotExistError
        
        item_creator = await queries.get_item_creator(
            self.connection,
            item_id=item_id
        )
        if item_creator != user_id:
            raise NoEnoughPriviligesError

        await queries.delete_item(
            self.connection,
            item_id=item_id
        )
        await self.connection.commit()
