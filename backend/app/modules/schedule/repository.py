import uuid
from collections.abc import Sequence

from app.core.repository import BaseRepository
from app.modules.schedule.models import Stage


class StageRepository(BaseRepository[Stage]):
    model = Stage
    default_order_by = (Stage.code,)

    async def list_by_site(self, site_id: uuid.UUID) -> Sequence[Stage]:
        return await self.list_by(site_id=site_id)

    async def delete_by_site(self, site_id: uuid.UUID) -> None:
        await self.delete_by(site_id=site_id)
