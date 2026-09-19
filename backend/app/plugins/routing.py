from fastapi import APIRouter

from app.modules.schedule.router import router as schedule_router
from app.modules.site.router import router as site_router
from app.modules.status.router import router as status_router
from app.modules.user.router import router as user_router
from app.modules.utility.router import router as utility_router

api_router = APIRouter()
api_router.include_router(utility_router)
api_router.include_router(site_router)
api_router.include_router(schedule_router)
api_router.include_router(status_router)
api_router.include_router(user_router)
