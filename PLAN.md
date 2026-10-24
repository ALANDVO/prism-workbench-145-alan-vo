# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

project-skeleton

## Roadmap

### project-skeleton — Project Skeleton with FastAPI/React

Status: done

Acceptance:
- FastAPI backend with SQLite runs locally
- React + TypeScript + Vite frontend builds
- Dockerfiles and docker-compose.yml work
- Basic health check endpoint responds
- Frontend loads and shows app name

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/core/database.py`, `backend/app/models/agent_task.py`, `backend/app/api/health.py`, `backend/app/api/agents.py`, `backend/app/api/tasks.py`, `backend/app/api/schemas.py`, `backend/requirements.txt`, `backend/Dockerfile`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tsconfig.node.json`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`, `frontend/src/components/Layout.tsx`, `frontend/src/components/Layout.css`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/pages/Dashboard.css`, `frontend/src/pages/Agents.tsx`, `frontend/src/pages/Agents.css`, `frontend/src/pages/Tasks.tsx`, `frontend/src/pages/Tasks.css`, `frontend/src/api/client.ts`, `frontend/src/api/index.ts`, `frontend/src/types/index.ts`, `frontend/nginx.conf`, `frontend/Dockerfile`, `docker-compose.yml`, `.env.example`, `.gitignore`, `README.md`, `LICENSE`, `CHANGELOG.md`, `portfolio.json`

Tests: `backend/app/tests/test_api.py`, `frontend/vitest.config.ts`, `frontend/src/test/setup.ts`, `frontend/src/App.test.tsx`

### agent-task-core — Agent Task Management Core

Status: done

Acceptance:
- CRUD API for agents and tasks with persistence
- Agent heartbeat endpoint for work polling
- Task assignment to agents with status transitions
- Frontend dashboard showing agents, tasks, and assignments

Implementation: `backend/app/models/agent_task.py`, `backend/app/api/agents.py`, `backend/app/api/tasks.py`, `backend/app/api/schemas.py`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/pages/Agents.tsx`, `frontend/src/pages/Tasks.tsx`

Tests: `backend/app/tests/test_api.py`

### org-chart-governance — Org Chart & Governance

Status: planned

Acceptance:
- Hierarchical agent org chart with roles
- Approval gates for task completion
- Budget tracking per agent/project

### skills-training — Skills & Training Studio

Status: planned

Acceptance:
- Shared skill library with versioning
- Skill testing with saved inputs
- Agent skill assignment

### oidc-auth — OIDC/Keycloak Authentication

Status: planned

Acceptance:
- Keycloak integration with PKCE flow
- Role-based access control (viewer/operator/admin)
- Protected API endpoints

### llm-adapters — LLM Provider Adapters

Status: planned

Acceptance:
- OpenAI-compatible, Anthropic, Gemini, Ollama adapters
- Configurable provider/model/endpoint
- Advisory explanations grounded in records

### routines-scheduling — Routines & Scheduling

Status: planned

Acceptance:
- Scheduled recurring tasks
- Webhook/API trigger support
- Run history and audit trail

### packaging-docs — Packaging, Docs & CI

Status: planned

Acceptance:
- Complete README with Mermaid diagram
- CHANGELOG, LICENSE, portfolio.json
- GitHub Actions CI workflow
- Docker healthchecks

Implementation: `README.md`, `LICENSE`, `CHANGELOG.md`, `portfolio.json`, `backend/Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`

