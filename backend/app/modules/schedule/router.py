import uuid

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.modules.schedule.schemas import ScheduleImport, StageRead
from app.modules.schedule.service import ScheduleService

router = APIRouter(prefix="/sites/{site_id}/schedule", tags=["schedule"])


@router.get("")
@inject
async def list_stages(site_id: uuid.UUID, service: FromDishka[ScheduleService]) -> list[StageRead]:
    stages = await service.list_stages(site_id)
    return [StageRead.model_validate(stage) for stage in stages]


@router.put("")
@inject
async def import_schedule(
    site_id: uuid.UUID, data: ScheduleImport, service: FromDishka[ScheduleService]
) -> list[StageRead]:
    stages = await service.import_schedule(site_id, data)
    return [StageRead.model_validate(stage) for stage in stages]
