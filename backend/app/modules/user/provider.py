from dishka import Provider, Scope, provide

from app.modules.user.repository import UserRepository
from app.modules.user.service import UserService


class UserProvider(Provider):
    scope = Scope.REQUEST

    repository = provide(UserRepository)
    service = provide(UserService)
