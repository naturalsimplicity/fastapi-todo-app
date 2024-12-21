from pydantic import BaseModel, Field
from typing import Annotated


class User(BaseModel):
    id_: Annotated[int, Field('ID of a user', alias="id")]
    login: Annotated[str, Field('User login')]
    name: Annotated[str, Field(title='User name', min_length=1, max_length=255)]
    