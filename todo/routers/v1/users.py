from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import Annotated

from todo.dependencies.database import get_repository
from todo.models.schemas.users import UserOnCreate, UserOnCreateResponse
from todo.repositories.users import UsersRepository
from todo.database.errors import LoginIsUnavailable
from todo.resources import strings

router = APIRouter(
    prefix="/users"
)

@router.post("/")
async def create_user(
    user: UserOnCreate,
    user_repo: Annotated[UsersRepository, Depends(get_repository(UsersRepository))]
) -> UserOnCreateResponse:
    try:
        id_ = await user_repo.create_user(
            login=user.login,
            name=user.name
        )
    except LoginIsUnavailable:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=strings.LOGIN_IS_ALREADY_USED
        )
    return UserOnCreateResponse(id=id_)
