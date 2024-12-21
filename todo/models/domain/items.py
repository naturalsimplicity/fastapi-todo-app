from pydantic import BaseModel, Field
from typing import Annotated


class Item(BaseModel):
    id_: Annotated[int, Field(title='Id of a task', alias="id")]
    user_id: Annotated[int, Field('Id of the user created the task')]
    title: Annotated[str, Field(title='Name of a task', min_length=1, max_length=255)]
    description: Annotated[str | None, Field(title='Description of a task', default=None)]
    completed: Annotated[bool, Field(title='Is completed task', default=False)]
