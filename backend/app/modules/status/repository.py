import uuid
from collections.abc import Sequence
from datetime import date

from sqlalchemy import delete, select

from app.core.repository import BaseRepository
from app.modules.schedule.models import Stage
from app.modules.status.models import StageStatus


class StageStatusRepository(BaseRepository[StageStatus]):
    model = StageStatus

    async def list_by_site(self, site_id: uuid.UUID, as_of: date) -> Sequence[StageStatus]:
        statement = (
            select(StageStatus)
            .join(Stage, Stage.id == StageStatus.stage_id)
            .where(Stage.site_id == site_id, StageStatus.as_of == as_of)
            .order_by(Stage.code)
        )
        result = await self._session.execute(statement)
        return result.scalars().all()

    async def delete_by_site(self, site_id: uuid.UUID, as_of: date) -> None:
        stage_ids = select(Stage.id).where(Stage.site_id == site_id)
        await self._session.execute(
            delete(StageStatus).where(
                StageStatus.stage_id.in_(stage_ids), StageStatus.as_of == as_of
            )
        )
        await self._session.flush()
