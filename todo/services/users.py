from aiosqlite import Connection
from datetime import datetime, timedelta
from pydantic import ValidationError
import jwt

from todo.services.base import BaseService
from todo.database.queries import queries
from todo.models.users import User, UserWithToken, UserTokenStatus
from todo.core.settings import settings
from todo.exceptions import InvalidTokenError, TokenHasExpiredError, LoginIsUnavailableError


class UserService(BaseService):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)

    @staticmethod
    def create_token_for_user(
        user_id: int,
        secret_key: str
    ) -> str:
        to_encode = {
            'id': user_id,
            'expire': datetime.strftime(
                datetime.now() + timedelta(seconds=settings.access_token_expire_seconds),
                '%Y-%m-%d %H:%M:%S'
            )
        }
        return jwt.encode(to_encode, secret_key, algorithm=settings.encryption_algorithm)
    
    @staticmethod
    def get_user_from_token(
        token: str,
        secret_key: str
    ) -> User:
        try:
            user = UserTokenStatus(**jwt.decode(token, secret_key, algorithms=[settings.encryption_algorithm]))
            if user.expire < datetime.now():
                raise TokenHasExpiredError
            return User(id=user.id_)
        except jwt.PyJWTError as decode_error:
            raise InvalidTokenError("unable to decode JWT token") from decode_error
        except ValidationError as validation_error:
            raise InvalidTokenError("malformed payload in token") from validation_error
        
    async def create_user(
        self,
        login: str,
        name: str
    ) -> UserWithToken:
        if await queries.check_login_availability(
            self.connection,
            login=login
        ):
            raise LoginIsUnavailableError(f"Login {login} is already used")
        
        user_id = await queries.create_new_user(
            self.connection,
            login=login,
            name=name
        )
        await self.connection.commit()

        token = self.create_token_for_user(
            user_id=user_id,
            secret_key=settings.secret_key
        )
        return UserWithToken(
            id=user_id,
            token=token
        )
    