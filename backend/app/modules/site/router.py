import uuid

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.modules.site.schemas import SiteCreate, SiteRead
from app.modules.site.service import SiteService

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("")
@inject
async def list_sites(service: FromDishka[SiteService]) -> list[SiteRead]:
    sites = await service.list_sites()
    return [SiteRead.model_validate(site) for site in sites]


@router.post("", status_code=201)
@inject
async def create_site(data: SiteCreate, service: FromDishka[SiteService]) -> SiteRead:
    site = await service.create_site(data)
    return SiteRead.model_validate(site)


@router.get("/{site_id}")
@inject
async def get_site(site_id: uuid.UUID, service: FromDishka[SiteService]) -> SiteRead:
    site = await service.get_site(site_id)
    return SiteRead.model_validate(site)
