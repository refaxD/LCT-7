import uuid
from collections.abc import Sequence
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.schedule.models import Stage
from app.modules.schedule.repository import StageRepository
from app.modules.site.models import Site
from app.modules.site.repository import SiteRepository
from app.modules.status.enums import StageStatusValue
from app.modules.status.models import StageStatus
from app.modules.status.repository import StageStatusRepository
from app.modules.status.schemas import SiteStatusUpsert
from app.plugins.exceptions import AppError


class StageStatusService:
    def __init__(
        self,
        repository: StageStatusRepository,
        stage_repository: StageRepository,
        site_repository: SiteRepository,
        session: AsyncSession,
    ) -> None:
        self._repository = repository
        self._stage_repository = stage_repository
        self._site_repository = site_repository
        self._session = session

    async def get_site_status(
        self, site_id: uuid.UUID, as_of: date
    ) -> tuple[Site, Sequence[StageStatus]]:
        site = await self._require_site(site_id)
        return site, await self._repository.list_by_site(site_id, as_of)

    async def replace_site_status(
        self, site_id: uuid.UUID, data: SiteStatusUpsert
    ) -> tuple[Site, Sequence[StageStatus]]:
        site = await self._require_site(site_id)
        stages = {stage.code: stage for stage in await self._stage_repository.list_by_site(site_id)}

        unknown = sorted({item.stage_code for item in data.stages if item.stage_code not in stages})
        if unknown:
            raise AppError(f"Этих этапов нет в графике: {', '.join(unknown)}", status_code=422)

        for item in data.stages:
            self._check_observability(stages[item.stage_code], item.status)

        await self._repository.delete_by_site(site_id, data.as_of)
        for item in data.stages:
            await self._repository.add(
                StageStatus(
                    stage_id=stages[item.stage_code].id,
                    as_of=data.as_of,
                    status=item.status.value,
                    delay_days=item.delay_days,
                    basis=item.basis,
                    confidence=item.confidence.value if item.confidence else None,
                    evidence_dates=[day.isoformat() for day in item.evidence_dates],
                )
            )

        await self._session.commit()
        return site, await self._repository.list_by_site(site_id, data.as_of)

    @staticmethod
    def _check_observability(stage: Stage, status: StageStatusValue) -> None:
        """CONTRACTS §2: на непроверяемом по технике этапе вывод — not_checkable, а не нарушение."""
        not_checkable = status is StageStatusValue.NOT_CHECKABLE
        if stage.checkable_by_equipment and not_checkable:
            raise AppError(
                f"Этап {stage.code} проверяется по технике — not_checkable недопустим",
                status_code=422,
            )
        if not stage.checkable_by_equipment and not not_checkable:
            raise AppError(
                f"Этап {stage.code} по технике не проверяется — допустим только not_checkable",
                status_code=422,
            )

    async def _require_site(self, site_id: uuid.UUID) -> Site:
        site = await self._site_repository.get(site_id)
        if site is None:
            raise AppError("Стройка не найдена", status_code=404)
        return site
