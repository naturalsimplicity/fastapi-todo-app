from pydantic import BaseModel, Field


class ItemOnCreate(BaseModel):
    title: str = Field(
        title='Name of a task',
        min_length=1,
        max_length=255
    )
    description: str | None = Field(
        title='Description of a task',
        default=None
    )
    completed: bool = Field(
        title='Is completed task',
        default=False
    )

class ItemID(BaseModel):
    id_: int = Field(
        alias="id",
        title="ID of created task"
    )

class ItemUserID(BaseModel):
    user_id: int = Field(
        title='Id of the user created the task'
    )

class Item(ItemOnCreate, ItemID, ItemUserID):
    ...
