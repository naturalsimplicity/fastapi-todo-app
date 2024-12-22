from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status
from typing import Annotated, Callable

from todo.dependencies.database import get_service
from todo.services.users import UserService
from todo.models.users import User
from todo.core.settings import get_app_settings, AppSettings
from todo.resources import strings
from todo.exceptions import InvalidTokenError, TokenHasExpiredError

HEADER_KEY = 'Authorization'

def _get_authorization_header(
    token: Annotated[str, Security(APIKeyHeader(name=HEADER_KEY))]
) -> str:
    return token

async def _get_current_user(
    token: Annotated[str, Depends(_get_authorization_header)],
    user_service: Annotated[UserService, Depends(get_service(UserService))],
    settings: Annotated[AppSettings, Depends(get_app_settings)]
) -> User:
    try:
        return user_service.get_user_from_token(
            token=token,
            secret_key=settings.secret_key
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )
    except TokenHasExpiredError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.AUTHENTICATION_TOKEN_HAS_EXPIRED,
        )

def get_current_user() -> Callable:
    return _get_current_user
