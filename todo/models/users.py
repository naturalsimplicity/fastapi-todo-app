from pydantic import BaseModel, Field
from datetime import datetime


class UserOnCreate(BaseModel):
    name: str
    login: str


class User(BaseModel):
    id_: int = Field(alias='id')

class UserTokenStatus(User):
    expire: datetime

class UserWithToken(User):
    token: str
