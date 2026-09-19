from fastapi import APIRouter

from app.modules.user.router import router as user_router
from app.modules.utility.router import router as utility_router

api_router = APIRouter()
api_router.include_router(utility_router)
api_router.include_router(user_router)
