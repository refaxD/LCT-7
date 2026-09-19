"""Репозиторий только стейджит изменения: commit — ответственность сервиса."""

import uuid
from collections.abc import Sequence
from typing import Any

from sqlalchemy import ColumnExpressionArgument, Select, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base


class BaseRepository[ModelT: Base]:
    model: type[ModelT]
    default_order_by: Sequence[ColumnExpressionArgument[Any]] = ()

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _select(self) -> Select[tuple[ModelT]]:
        statement = select(self.model)
        if self.default_order_by:
            statement = statement.order_by(*self.default_order_by)
        return statement

    async def list(self) -> Sequence[ModelT]:
        result = await self._session.execute(self._select())
        return result.scalars().all()

    async def get(self, entity_id: uuid.UUID) -> ModelT | None:
        return await self._session.get(self.model, entity_id)

    async def get_by(self, **filters: Any) -> ModelT | None:
        result = await self._session.execute(select(self.model).filter_by(**filters))
        return result.scalar_one_or_none()

    async def list_by(self, **filters: Any) -> Sequence[ModelT]:
        result = await self._session.execute(self._select().filter_by(**filters))
        return result.scalars().all()

    async def add(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def delete(self, entity: ModelT) -> None:
        await self._session.delete(entity)
        await self._session.flush()

    async def delete_by(self, **filters: Any) -> None:
        await self._session.execute(delete(self.model).filter_by(**filters))
        await self._session.flush()
