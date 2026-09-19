from collections.abc import AsyncIterable

from dishka import AsyncContainer, Provider, Scope, make_async_container, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import Settings, get_settings
from app.modules.user.provider import UserProvider


class AppProvider(Provider):
    scope = Scope.APP

    @provide
    def settings(self) -> Settings:
        return get_settings()


class DatabaseProvider(Provider):
    scope = Scope.APP

    @provide
    async def engine(self, settings: Settings) -> AsyncIterable[AsyncEngine]:
        engine = create_async_engine(settings.postgres.url, pool_pre_ping=True)
        yield engine
        await engine.dispose()

    @provide
    def sessionmaker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def session(self, maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with maker() as session:
            yield session


def create_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        DatabaseProvider(),
        UserProvider(),
    )
