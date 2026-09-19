from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.modules.user.schemas import UserCreate, UserRead
from app.modules.user.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
@inject
async def list_users(service: FromDishka[UserService]) -> list[UserRead]:
    users = await service.list_users()
    return [UserRead.model_validate(user) for user in users]


@router.post("", status_code=201)
@inject
async def create_user(data: UserCreate, service: FromDishka[UserService]) -> UserRead:
    user = await service.create_user(data)
    return UserRead.model_validate(user)
