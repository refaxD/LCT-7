import uuid
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.site.models import Site
from app.modules.site.repository import SiteRepository
from app.modules.site.schemas import SiteCreate
from app.plugins.exceptions import AppError


class SiteService:
    def __init__(self, repository: SiteRepository, session: AsyncSession) -> None:
        self._repository = repository
        self._session = session

    async def list_sites(self) -> Sequence[Site]:
        return await self._repository.list()

    async def get_site(self, site_id: uuid.UUID) -> Site:
        site = await self._repository.get(site_id)
        if site is None:
            raise AppError("Стройка не найдена", status_code=404)
        return site

    async def create_site(self, data: SiteCreate) -> Site:
        if await self._repository.get_by_code(data.code):
            raise AppError(f"Стройка с кодом {data.code} уже заведена", status_code=409)

        site = Site(code=data.code, name=data.name)
        await self._repository.add(site)
        await self._session.commit()
        return site
