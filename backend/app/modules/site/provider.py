from dishka import Provider, Scope, provide

from app.modules.site.repository import SiteRepository
from app.modules.site.service import SiteService


class SiteProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(SiteRepository)
    service = provide(SiteService)
