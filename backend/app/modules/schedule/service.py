import uuid
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.schedule.models import Stage
from app.modules.schedule.repository import StageRepository
from app.modules.schedule.schemas import ScheduleImport
from app.modules.site.repository import SiteRepository
from app.plugins.exceptions import AppError


class ScheduleService:
    def __init__(
        self,
        repository: StageRepository,
        site_repository: SiteRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._site_repository = site_repository
        self._session = session

    async def list_stages(self, site_id: uuid.UUID) -> Sequence[Stage]:
        await self._require_site(site_id)
        return await self._repository.list_by_site(site_id)

    async def import_schedule(self, site_id: uuid.UUID, data: ScheduleImport) -> Sequence[Stage]:
        """Импорт заменяет график целиком: статусы старых этапов уходят по каскаду."""
        await self._require_site(site_id)

        codes = [stage.code for stage in data.stages]
        duplicates = sorted({code for code in codes if codes.count(code) > 1})
        if duplicates:
            raise AppError(f"Коды этапов повторяются: {', '.join(duplicates)}", status_code=422)

        for stage in data.stages:
            if (
                stage.planned_start
                and stage.planned_end
                and stage.planned_end < stage.planned_start
            ):
                raise AppError(
                    f"Этап {stage.code}: плановое окончание раньше начала", status_code=422
                )

        await self._repository.delete_by_site(site_id)
        for stage in data.stages:
            await self._repository.add(Stage(site_id=site_id, **stage.model_dump()))

        await self._session.commit()
        return await self._repository.list_by_site(site_id)

    async def _require_site(self, site_id: uuid.UUID) -> None:
        if await self._site_repository.get(site_id) is None:
            raise AppError("Стройка не найдена", status_code=404)
