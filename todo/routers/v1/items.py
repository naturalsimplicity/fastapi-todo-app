from fastapi import APIRouter, Depends, Path, HTTPException
from starlette import status
from typing import Annotated

from todo.models.items import ItemOnCreate, Item, ItemID
from todo.models.users import UserWithToken
from todo.services.items import ItemService
from todo.dependencies.database import get_service
from todo.dependencies.auth import get_current_user
from todo.resources import strings
from todo.exceptions import ItemDoesNotExistError, NoEnoughPriviligesError

router = APIRouter(
    prefix="/items",
    tags=['Items']
)

@router.post("/")
async def create_item(
    item: ItemOnCreate,
    user: Annotated[UserWithToken, Depends(get_current_user())],
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> ItemID:
    return await item_service.create_item(
        user_id=user.id_,
        title=item.title,
        description=item.description,
        completed=item.completed
    )

@router.get("/{item_id}")
async def get_item(
    item_id: Annotated[
        int,
        Path(
            title="Id of an item",
            examples=[1]
        )
    ],
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> Item:
    try:
        return await item_service.get_item(
            item_id=item_id
        )
    except ItemDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ITEM_DOES_NOT_EXIST
        )

@router.get("/")
async def get_items(
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> list[Item]:
    return await item_service.get_items()

@router.put("/{item_id}")
async def update_item(
    item_id: Annotated[
        int,
        Path(
            title="Id of an item",
            examples=[1]
        )
    ],
    item: ItemOnCreate,
    user: Annotated[UserWithToken, Depends(get_current_user())],
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> None:
    try:
        return await item_service.update_item(
            item_id=item_id,
            user_id=user.id_,
            title=item.title,
            description=item.description,
            completed=item.completed
        )
    except ItemDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ITEM_DOES_NOT_EXIST
        )
    except NoEnoughPriviligesError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CANNOT_MODIFY_ITEMS
        )
    
@router.delete("/{item_id}")
async def delete_item(
    item_id: Annotated[
        int,
        Path(
            title="Id of an item",
            examples=[1]
        )
    ],
    user: Annotated[UserWithToken, Depends(get_current_user())],
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> None:
    try:
        return await item_service.delete_item(
            item_id=item_id,
            user_id=user.id_
        )
    except ItemDoesNotExistError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ITEM_DOES_NOT_EXIST
        )
    except NoEnoughPriviligesError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CANNOT_MODIFY_ITEMS
        )
    