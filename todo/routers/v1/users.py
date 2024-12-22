from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import Annotated

from todo.dependencies.database import get_service
from todo.models.users import UserOnCreate, UserWithToken
from todo.models.items import Item
from todo.services.users import UserService
from todo.services.items import ItemService
from todo.exceptions import LoginIsUnavailableError
from todo.resources import strings

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/register")
async def create_user(
    user: UserOnCreate,
    user_service: Annotated[UserService, Depends(get_service(UserService))]
) -> UserWithToken:
    try:
        return await user_service.create_user(
            login=user.login,
            name=user.name
        )

        return 
    except LoginIsUnavailableError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=strings.LOGIN_IS_ALREADY_USED
        )
    
@router.get("/{login}/items")
async def get_user_items(
    login: Annotated[
        str,
        Path(
            title="User login",
            examples=["matvey"],
            min_length=1
        )
    ],
    item_service: Annotated[ItemService, Depends(get_service(ItemService))]
) -> list[Item]:
    return await item_service.get_items(
        login=login
    )

