from dishka import Provider, Scope, provide

from app.modules.status.repository import StageStatusRepository
from app.modules.status.service import StageStatusService


class StageStatusProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(StageStatusRepository)
    service = provide(StageStatusService)
