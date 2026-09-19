from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password
from app.modules.user.models import User
from app.modules.user.repository import UserRepository
from app.modules.user.schemas import UserCreate
from app.plugins.exceptions import AppError


class UserService:
    def __init__(self, repository: UserRepository, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    async def list_users(self) -> Sequence[User]:
        return await self._repository.list()

    async def create_user(self, data: UserCreate) -> User:
        if await self._repository.get_by_email(data.email):
            raise AppError("Пользователь с таким email уже существует", status_code=409)

        user = User(
            email=data.email,
            name=data.name,
            role=data.role,
            hashed_password=hash_password(data.password),
        )
        await self._repository.add(user)
        await self._session.commit()
        return user
