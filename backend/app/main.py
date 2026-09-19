from contextlib import asynccontextmanager

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.core.settings import get_settings
from app.plugins.di import create_container
from app.plugins.exceptions import register_exception_handlers
from app.plugins.routing import api_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Схема БД накатывается миграциями Alembic (`alembic upgrade head`) до старта
    # сервера — см. команду запуска в deploy/docker/dev/core.yaml и Dockerfile.
    yield
    await app.state.dishka_container.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="LCT-7 API",
        docs_url=f"{settings.api_prefix}/docs",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        lifespan=lifespan,
    )

    container = create_container()
    setup_dishka(container, app)

    register_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
