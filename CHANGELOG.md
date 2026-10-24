# Changelog

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
