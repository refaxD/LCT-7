from app.core.repository import BaseRepository
from app.modules.site.models import Site


class SiteRepository(BaseRepository[Site]):
    model = Site
    default_order_by = (Site.code,)

    async def get_by_code(self, code: str) -> Site | None:
        return await self.get_by(code=code)
