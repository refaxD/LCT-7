from fastapi import APIRouter

from app.modules.utility.schemas import HealthResponse

router = APIRouter(tags=["utility"])


@router.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="ok")
