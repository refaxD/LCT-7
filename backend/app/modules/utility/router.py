from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.utility.schemas import HealthResponse

router = APIRouter(tags=["utility"])


@router.get("/health")
@inject
async def health(session: FromDishka[AsyncSession], response: Response) -> HealthResponse:
    """Traefik и деплой считают сервис живым по этому ответу — без БД он не живой."""
    try:
        await session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return HealthResponse(status="degraded", database="down")

    return HealthResponse(status="ok", database="ok")
