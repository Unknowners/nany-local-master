Title: Cursor Workspace Guide — nanny-match-ukraine (frontend) + nanny-match-backend (FastAPI)

Overview

This workspace contains two separate GitHub repositories:
Frontend: nanny-match-ukraine (React + Vite + Tailwind + TypeScript)
Backend: nanny-match-backend (FastAPI + Python)
Goal: enable smooth parallel development in Cursor/VS Code, with strict separation of commits per repo, cross-repo synchronization, and human-readable documentation for every change.
Workspace Layout (recommended)

workspace-root/
CURSOR_WORKSPACE.md (this file)
nanny-match-ukraine/ (frontend repo)
nanny-match-backend/ (backend repo)
optional: data/ or docs/ (shared planning notes, not a repo)
workspace.code-workspace (optional, to open both repos at once in Cursor/VS Code)
GitHub Repositories

Frontend repository
Name: nanny-match-ukraine
Tech: React 18, Vite, Tailwind CSS, TypeScript, Shadcn UI, Supabase client, optional FastAPI adapter
Backend repository
Name: nanny-match-backend
Tech: FastAPI, Uvicorn, Pydantic, SQL/ORM/migrations (e.g., Alembic), JWT auth, optional Supabase integration for storage/auth if desired
Strict rule: commit changes separately in each repository. If a change spans both repos, create two commits and two PRs—one per repo—and link them to each other.
Quick Start (per repository)

Frontend (nanny-match-ukraine):
Requirements: Node 18+ (or 20+), npm or pnpm
Install and run:
npm install
npm run dev
Environment (.env, example):
VITE_BACKEND_KIND=supabase or fastapi
VITE_SUPABASE_URL=…
VITE_SUPABASE_ANON_KEY=…
VITE_FASTAPI_BASE_URL=http://localhost:8000
VITE_FASTAPI_API_KEY=dev-…
Backend (nanny-match-backend):
Requirements: Python 3.11+, uvicorn, pip or uv
Install and run:
python -m venv .venv && source .venv/bin/activate (Windows: .venv\Scripts\activate)
pip install -r requirements.txt (or uv pip/poetry)
uvicorn app.main:app --reload --port 8000
Environment (.env, example):
APP_ENV=development
API_KEY=dev-…
DATABASE_URL=postgresql://user:pass@localhost:5432/nanny_db
JWT_SECRET=super-secret
CORS_ORIGINS=http://localhost:5173
Backend Switching (Frontend)

Options supported:
Env-based (recommended for local/dev CI):
Set VITE_BACKEND_KIND=supabase or fastapi
For FastAPI, set VITE_FASTAPI_BASE_URL and VITE_FASTAPI_API_KEY
LocalStorage-based (dev convenience):
In browser console:
localStorage.setItem('backend-kind', 'fastapi')
localStorage.setItem('fastapi-base-url', 'http://localhost:8000')
localStorage.setItem('fastapi-api-key', 'dev-…')
The frontend already includes ports/adapters architecture:
packages/ports/src/BackendPort.ts
packages/adapters/fastapi/src/index.ts (frontend FastAPI adapter)
Important Files and Folders (Frontend: nanny-match-ukraine)

Project entry and routing:
src/main.tsx
src/App.tsx
src/pages/* (all routes)
Auth and backend integrations:
src/contexts/AuthContext.tsx
src/integrations/supabase/client.ts
packages/ports/src/BackendPort.ts
packages/adapters/fastapi/src/index.ts
UI and components:
src/components/* (app components)
src/components/ui/* (Shadcn UI; avoid manual edits, add via generator)
Onboarding system:
src/components/onboarding/*
src/hooks/useDynamicOnboarding.tsx
Docs and guides:
FRONTEND_DEVELOPMENT_GUIDE.md (keep updated)
FASTAPI_BACKEND_GUIDE.md (high-level API contract reference for frontend devs)
Build/config:
package.json, vite.config.ts, tsconfig.json, tailwind.config.ts
.env and .env.example
Important Files and Folders (Backend: nanny-match-backend)

FastAPI app structure (recommended):
app/main.py (FastAPI app entry)
app/api/ (routers)
app/schemas/ (Pydantic models)
app/models/ (DB models if using ORM)
app/services/ (business logic)
app/auth/ (JWT, session)
migrations/ (Alembic)
tests/
requirements.txt or pyproject.toml
.env and .env.example
Docs and guides:
FASTAPI_BACKEND_GUIDE.md (API, endpoints, security, storage, realtime)
API contract: docs/api/openapi.yaml or auto-generated OpenAPI at /docs
Data and schema (if you maintain SQL separately):
Keep schema docs or SQL files under backend repo in db/ or data/ (e.g., enums.sql, tables.sql, seed-data)
Align with any existing fastapi-backend-data content you already maintain
Cross-Repo Synchronization Rules

Separate commits and PRs:
Frontend changes go to nanny-match-ukraine
Backend changes go to nanny-match-backend
Cross-reference PRs:
Example PR description: “Companion PR: https://github.com/org/nanny-match-backend/pull/123”
Conventional Commits (recommended):
feat:, fix:, docs:, refactor:, chore:, test:, perf:, build:, ci:, revert:
Examples:
feat(api): add /bookings/availability endpoint
fix(ui): debounce search input for nannies list
API contract changes:
Update backend routers, schemas, and OpenAPI
Update frontend adapter (packages/adapters/fastapi/src/index.ts) and types
Update human-readable docs (see Documentation Rules)
Verify end-to-end manually (see Verification Checklist)
DB changes:
Add migration scripts (backend)
Update seed/reference data if applicable
Document breaking/non-breaking impacts
Communicate required environment changes
Documentation Rules (Human-Readable, Required)

For every change that affects behavior, API, data, or UX, add an entry to docs/CHANGELOG.md in the repo where the change occurs.
If a change affects both repos, add entries in both CHANGELOGs and link to the companion PR.
Keep entries short, precise, and understandable for non-technical stakeholders.
Use the template below for each entry (Cursor should auto-insert this when creating or updating a feature).
CHANGELOG template (docs/CHANGELOG.md entry)

Date: YYYY-MM-DD
Title: short description
Repos affected: frontend/backend/both
Summary:
What changed and why (1–3 bullets)
Files touched (high-level):
path/to/file1
path/to/file2
API/DB impact:
Endpoints added/changed/removed
Request/response shape changes
Migrations applied (ID)
Frontend impact:
UI components/pages affected
Rollout notes:
Env vars, feature flags, data migrations, steps
Pull Request Template (.github/PULL_REQUEST_TEMPLATE.md)

Summary:
What and why (1–3 sentences)
Type:
feat / fix / chore / docs / refactor / test / perf / build / ci / revert
Linked Issues:
Closes #…
Companion PRs:
nanny-match-ukraine: …
nanny-match-backend: …
Screenshots (if UI)
Testing:
Steps to verify
Checklist:
[ ] CHANGELOG updated
[ ] Env doc updated if needed
[ ] API contract updated (OpenAPI, guide)
[ ] No breaking changes, or breaking changes documented
What Cursor Should Auto-Create/Update

In nanny-match-ukraine (frontend repo):
docs/CHANGELOG.md (create if missing)
.github/PULL_REQUEST_TEMPLATE.md
Keep FRONTEND_DEVELOPMENT_GUIDE.md up to date
If API changes, update:
packages/ports/src/BackendPort.ts (if the interface evolves)
packages/adapters/fastapi/src/index.ts (frontend adapter)
src/integrations/supabase/client.ts (if switching or dual-mode behavior changes)
In nanny-match-backend (backend repo):
docs/CHANGELOG.md (create if missing)
.github/PULL_REQUEST_TEMPLATE.md
Maintain FASTAPI_BACKEND_GUIDE.md (endpoints, auth, storage, realtime)
docs/api/openapi.yaml (optional, or rely on auto-generated /docs)
Verification Checklist (Before merge)

Backend:
Local server runs: uvicorn app.main:app --reload
New/changed endpoints appear in /docs
Migrations run locally; seed data applied if needed
Frontend:
npm run dev renders without errors
API calls succeed against the selected backend
Key flows tested (auth, onboarding, bookings)
Docs:
CHANGELOG updated (with template)
Companion PR is linked and synchronized
Env notes added if anything changed
Environment and Secrets

Frontend:
.env and .env.example must be kept in sync
Required vars: VITE_BACKEND_KIND, VITE_SUPABASE_URL/VITE_SUPABASE_ANON_KEY (if using Supabase), VITE_FASTAPI_BASE_URL/VITE_FASTAPI_API_KEY (if using FastAPI)
Backend:
.env and .env.example must be kept in sync
Typical vars: API_KEY, DATABASE_URL, JWT_SECRET, CORS_ORIGINS
Never commit real secrets. Only commit .env.example.
Optional: Multi-root Workspace File (workspace.code-workspace)

Place this file in workspace-root/ to open both repos in Cursor/VS Code: { "folders": [ { "path": "nanny-match-ukraine" }, { "path": "nanny-match-backend" } ], "settings": { "files.exclude": { "/.venv": true, "/node_modules": true, "/.idea": true, "/.DS_Store": true } } }
Conventions and Style

Commits: Conventional Commits
Branches: feature/…, fix/…, chore/… with short scope
Reviews: Cross-reference companion PRs
Releases: Tag both repos together for coordinated releases when API changes
References and Deep Links

Frontend (nanny-match-ukraine)
Entry: /nanny-match-ukraine/src/main.tsx, /nanny-match-ukraine/src/App.tsx
Ports/adapters: /nanny-match-ukraine/packages/ports/src/BackendPort.ts, /nanny-match-ukraine/packages/adapters/fastapi/src/index.ts
Supabase client: /nanny-match-ukraine/src/integrations/supabase/client.ts
Pages and components: /nanny-match-ukraine/src/pages/, /nanny-match-ukraine/src/components/
Guides: /nanny-match-ukraine/FRONTEND_DEVELOPMENT_GUIDE.md, /nanny-match-ukraine/FASTAPI_BACKEND_GUIDE.md
Backend (nanny-match-backend)
App entry (suggested): /nanny-match-backend/app/main.py
Routers: /nanny-match-backend/app/api/
Schemas: /nanny-match-backend/app/schemas/
Migrations: /nanny-match-backend/migrations/
Guides: /nanny-match-backend/FASTAPI_BACKEND_GUIDE.md
OpenAPI: /nanny-match-backend/docs/api/openapi.yaml (optional; also auto at /docs)
FAQ

Q: Can I mix commits touching both repos?
A: No. Make separate commits/PRs and link them. This keeps history clean and makes rollbacks safer.
Q: Where do I document small changes?
A: Every meaningful change gets a short entry in docs/CHANGELOG.md of the affected repo.
Q: How do I point the frontend to the backend?
A: Set VITE_BACKEND_KIND=fastapi and VITE_FASTAPI_BASE_URL; start FastAPI on that host:port.
Q: How do I revert a cross-repo change?
A: Revert both PRs, in reverse order of deployment, and document the rollback in both CHANGELOGs.
End of CURSOR_WORKSPACE.md

lov-plan

Add CURSOR_WORKSPACE.md at the root of this project (or update it if present) with the content above.
Create documentation scaffolding in this repo to guide future changes and mirror it in the backend repo:
docs/CHANGELOG.md (new file with an initial header and instructions)
.github/PULL_REQUEST_TEMPLATE.md (using the template above)
docs/templates/change-entry.md (store the CHANGELOG entry template for quick copy)
Add short pointers in FRONTEND_DEVELOPMENT_GUIDE.md and FASTAPI_BACKEND_GUIDE.md to refer to CURSOR_WORKSPACE.md for repo workflow, cross-repo sync, and docs rules.
Provide the same docs scaffolding content (as code blocks in a follow-up) for you to paste into the nanny-match-backend repo, or I can open PRs in both repos if they’re connected to Lovable.