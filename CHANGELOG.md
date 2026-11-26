# Changelog

## 1.6.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## [1.5.1] - 2026-11-26

### Added
- Org chart & governance: hierarchical agent org chart endpoint (`GET /agents/org-chart`) returning parent/child relationships with roles, status, and budget tracking
- Approval gates for task completion: parent agents can approve/reject tasks in `in_review` status, checking that the assignee has a parent agent

### Changed
- Moved org chart endpoint from tasks router to agents router to avoid route conflicts with `{task_id}` and `{agent_id}` parametric paths
- Enhanced `approve_task` and `reject_task` to explicitly validate org chain membership

### Fixed
- Route ordering conflict: org chart endpoint now registered before `{agent_id}` parametric routes in agents router
# Changelog

## 1.5.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.4.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.3.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

## 1.2.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Added
- Budget enforcement for task assignment and agent heartbeat
- Agent budget limit checking prevents over-assignment
- Tests for budget enforcement on assignment and heartbeat endpoints

## 1.1.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

### Fixed
- Pydantic V2 deprecation warnings: replaced class Config with model_config = ConfigDict(from_attributes=True, protected_namespaces=())
- datetime.utcnow() deprecation: replaced with timezone-aware datetime.now(timezone.utc) via utcnow() helper
- Unused import in frontend test setup

## 1.0.0 — work-in-progress checkpoint

Partial code published for continued development. Known issues: STATUS.md.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-10-24

### Added
- FastAPI backend with SQLite persistence
- React + TypeScript + Vite frontend
- Agent CRUD API with hierarchical support (parent/child relationships)
- Task CRUD API with status workflow (pending → assigned → in_progress → in_review → approved/rejected → completed/failed)
- Agent heartbeat endpoint for work polling
- Task assignment to agents with validation
- Task comments for collaboration
- Budget tracking per agent and per task
- Responsive dashboard with statistics
- Agents management page with modal forms
- Tasks management page with assignment dropdown
- Dockerfiles for backend and frontend
- Docker Compose with Keycloak for OIDC
- Health check endpoints
- Comprehensive backend tests
- Frontend typecheck and build scripts

### Security
- Demo mode binding to localhost only
- Environment-based configuration
- No hardcoded secrets

---

Alan Vo · [alanvo.net](https://alanvo.net) · [X: @alanvoasi](https://x.com/alanvoasi)
