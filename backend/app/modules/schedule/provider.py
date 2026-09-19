from dishka import Provider, Scope, provide

from app.modules.schedule.repository import StageRepository
from app.modules.schedule.service import ScheduleService


class ScheduleProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(StageRepository)
    service = provide(ScheduleService)
