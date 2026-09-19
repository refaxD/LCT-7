# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

LCT-7 is a hackathon monorepo for an automated construction-site violation detection service
(ДГП Москвы case). Three independent parts:

- `backend/` — FastAPI + Dishka (DI) + Granian (ASGI) + SQLAlchemy async + PostgreSQL, Alembic migrations.
- `frontend/` — React 19 + Vite 6 + TypeScript, single-page, served by nginx in prod.
- `ml/` — research + CLI tools for the vision/scheduling pipeline (YOLOE zero-shot detection). Standalone; not yet wired into the backend.

Orchestration is Docker Compose with layered files (`common` / `dev` / `prod`) behind Traefik.
`makefile` at the root is the entry point. Much of the code documentation is in Russian.

## Commands

Root (Docker Compose via `makefile`):

```bash
cp .env.dist .env   # first-time setup
make dev            # local: build + bind-mount + hot-reload (backend --reload, Vite dev-server)
make up             # prod images, no build
make deploy         # pull prod images by tag (deploy/versions.env) + up
make down           # stop, remove orphans
make logs           # follow logs
make pretty         # backend: ruff format + ruff check --fix
make check          # backend: ruff check + ruff format --check (CI/pre-commit)
make test           # backend: pytest (sqlite by default; TEST_DATABASE_URL to use postgres)
```