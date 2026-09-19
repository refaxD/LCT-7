# Одна стадия `build`: в dev на неё указывает target: build (dev/core.yaml) и
# монтирует исходники поверх; в prod образ используется как есть.
FROM python:3.12-slim AS build

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    # venv лежит вне /app, чтобы bind-mount исходников в dev его не перекрывал
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Слой зависимостей кешируется отдельно от исходников.
# --frozen: ставим ровно то, что в локе, и падаем, если лок разошёлся с pyproject
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000
# в проде тоже сначала миграции, потом сервер
CMD ["sh", "-c", "alembic upgrade head && granian --interface asgi app.main:app --host 0.0.0.0 --port 8000"]
