import uuid
from collections.abc import Sequence
from datetime import date
from typing import Annotated

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Query

from app.modules.site.models import Site
from app.modules.status.enums import Confidence, StageStatusValue
from app.modules.status.models import StageStatus
from app.modules.status.schemas import (
    PlannedWindow,
    SiteStatusRead,
    SiteStatusUpsert,
    StageStatusRead,
)
from app.modules.status.service import StageStatusService

router = APIRouter(prefix="/sites/{site_id}/status", tags=["status"])


def _to_read(site: Site, as_of: date, statuses: Sequence[StageStatus]) -> SiteStatusRead:
    return SiteStatusRead(
        site_id=site.code,
        as_of=as_of,
        stages=[
            StageStatusRead(
                stage_code=item.stage.code,
                stage_name=item.stage.name,
                planned=PlannedWindow(start=item.stage.planned_start, end=item.stage.planned_end),
                status=StageStatusValue(item.status),
                delay_days=item.delay_days,
                evidence_dates=[date.fromisoformat(day) for day in item.evidence_dates],
                basis=item.basis,
                confidence=Confidence(item.confidence) if item.confidence else None,
            )
            for item in statuses
        ],
    )


@router.get("")
@inject
async def get_site_status(
    site_id: uuid.UUID,
    service: FromDishka[StageStatusService],
    as_of: Annotated[date, Query(description="Дата, на которую собран вывод")],
) -> SiteStatusRead:
    site, statuses = await service.get_site_status(site_id, as_of)
    return _to_read(site, as_of, statuses)


@router.put("")
@inject
async def replace_site_status(
    site_id: uuid.UUID, data: SiteStatusUpsert, service: FromDishka[StageStatusService]
) -> SiteStatusRead:
    site, statuses = await service.replace_site_status(site_id, data)
    return _to_read(site, data.as_of, statuses)
