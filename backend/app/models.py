"""Единая точка импорта всех ORM-моделей — для Alembic (autogenerate).

При добавлении модуля с моделями допишите сюда импорт его models, иначе Alembic
их не «увидит» и не сгенерирует миграцию.
"""

from app.core.database import Base
from app.modules.schedule import models as schedule_models  # noqa: F401
from app.modules.site import models as site_models  # noqa: F401
from app.modules.status import models as status_models  # noqa: F401
from app.modules.user import models as user_models  # noqa: F401

__all__ = ["Base"]
