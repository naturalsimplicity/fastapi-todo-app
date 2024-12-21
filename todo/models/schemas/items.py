from pydantic import BaseModel


class ItemOnCreate(BaseModel):
    user_id: int
    title: str
    description: str | None
    completed: bool