# Product development plan

Each round completes one feature or repair. Future items are planned, not implemented claims.

## Current round

budget-enforcement

## Roadmap

### project-skeleton — Project Skeleton with FastAPI/React

Status: done

Acceptance:
- FastAPI backend with SQLite runs locally
- React + TypeScript + Vite frontend builds
- Dockerfiles and docker-compose.yml work
- Basic health check endpoint responds
- Frontend loads and shows app name

Implementation: `backend/app/main.py`, `backend/app/core/config.py`, `backend/app/core/database.py`, `backend/app/models/agent_task.py`, `backend/app/api/health.py`, `backend/app/api/agents.py`, `backend/app/api/tasks.py`, `backend/app/api/schemas.py`, `backend/requirements.txt`, `backend/Dockerfile`, `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/tsconfig.node.json`, `frontend/index.html`, `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/src/index.css`, `frontend/src/components/Layout.tsx`, `frontend/src/components/Layout.css`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/pages/Dashboard.css`, `frontend/src/pages/Agents.tsx`, `frontend/src/pages/Agents.css`, `frontend/src/pages/Tasks.tsx`, `frontend/src/pages/Tasks.css`, `frontend/src/api/client.ts`, `frontend/src/test/setup.ts`, `frontend/src/App.test.tsx`

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

### deprecation-fixes — Fix Pydantic V2 and datetime deprecation warnings

Status: done

Acceptance:
- Pydantic V2 ConfigDict replaces deprecated class Config
- protected_namespaces=() suppresses model_ field warnings
- datetime.utcnow() replaced with timezone-aware datetime.now(timezone.utc)
- All backend tests pass without deprecation warnings

Implementation: `backend/app/api/schemas.py`, `backend/app/models/agent_task.py`, `backend/app/api/tasks.py`, `frontend/src/test/setup.ts`

Tests: `backend/app/tests/test_api.py`, `frontend/src/App.test.tsx`

### budget-enforcement — Budget Enforcement for Task Assignment

Status: done

Acceptance:
- Agent budget limit prevents task assignment when budget would be exceeded
- Heartbeat endpoint checks budget before assigning work
- Agents with no budget limit (0) can accept unlimited tasks
- Comprehensive tests for assignment and heartbeat budget checks

Implementation: `backend/app/api/tasks.py`, `backend/app/tests/test_api.py`

Tests: `backend/app/tests/test_api.py::TestTaskAssignment::test_assign_task_budget_exceeded_fails`, `backend/app/tests/test_api.py::TestTaskAssignment::test_assign_task_budget_ok`, `backend/app/tests/test_api.py::TestTaskAssignment::test_assign_task_no_budget_limit_ok`, `backend/app/tests/test_api.py::TestHeartbeat::test_heartbeat_budget_exceeded`, `backend/app/tests/test_api.py::TestHeartbeat::test_heartbeat_budget_ok`, `backend/app/tests/test_api.py::TestHeartbeat::test_heartbeat_no_budget_limit_ok`

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

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
