from fastapi import APIRouter

from todo.routers.v1 import items, users


router = APIRouter(
    prefix='/v1'
)

router.include_router(items.router)
router.include_router(users.router)
