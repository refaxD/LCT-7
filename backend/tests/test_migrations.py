"""В проде схему накатывают миграции, а тесты создают её из Base.metadata.

Расхождение между этими двумя источниками тихое и дорогое: тесты зелёные,
а контейнер падает на старте. Этот тест применяет миграции к пустой базе
и сверяет результат с моделями.
"""

import importlib.util
from pathlib import Path
from types import ModuleType

import alembic
import pytest
from alembic.autogenerate import compare_metadata
from alembic.operations import Operations
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

from app.models import Base

VERSIONS = Path(__file__).resolve().parent.parent / "migrations" / "versions"


def _load(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(path.stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _paths() -> list[Path]:
    paths = sorted(VERSIONS.glob("[0-9]*.py"))
    assert paths, "миграций не найдено"
    return paths


def test_revisions_form_a_chain() -> None:
    previous: str | None = None
    for path in _paths():
        module = _load(path)
        assert module.down_revision == previous, f"{path.name}: разрыв цепочки ревизий"
        previous = module.revision


def test_migrations_match_models(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    engine = create_engine(f"sqlite:///{tmp_path / 'schema.db'}")

    with engine.begin() as connection:
        # Миграции берут `op` из модуля alembic — подменяем его на Operations
        # поверх нашего соединения, иначе upgrade() некуда выполнять.
        monkeypatch.setattr(alembic, "op", Operations(MigrationContext.configure(connection)))
        for path in _paths():
            _load(path).upgrade()

    with engine.connect() as connection:
        context = MigrationContext.configure(connection, opts={"compare_type": False})
        difference = compare_metadata(context, Base.metadata)

    assert difference == [], f"миграции разошлись с моделями: {difference}"

    engine.dispose()
