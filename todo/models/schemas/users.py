from pydantic import BaseModel, Field


class UserOnCreate(BaseModel):
    name: str
    login: str


class UserOnCreateResponse(BaseModel):
    id_: int = Field(alias='id')
    