# Launch Tracker

Track a product's journey from idea to launch — projects move through
`idea → mvp → beta → launch`, with milestones tracked and a live progress
percentage per project.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, SQLite
- **Frontend:** React

## Why this stack

- **FastAPI over Flask/Django** — async-ready, automatic OpenAPI docs
  (`/docs`), and Pydantic gives request/response validation for free instead
  of hand-rolling it.
- **SQLite for now** — zero setup, easy to run locally. Because the data
  layer only talks to SQLAlchemy's ORM (not raw SQL), moving to Postgres
  later is a one-line change to `database.py`, not a rewrite.
- **No auth in v1** — deliberately scoped out to keep this project focused
  and shippable in the time available. The route/schema/crud separation
  below means adding a `get_current_user` dependency later is additive, not
  a redesign.

## Architecture

```
backend/
├── main.py              # App setup, CORS, router registration
├── models.py             # SQLAlchemy models (Project, Milestone)
├── schemas.py             # Pydantic schemas — request/response validation
├── database.py            # DB engine/session setup
├── crud.py                # Data-access layer, no HTTP concerns
└── routes/
    └── projects.py         # HTTP layer — thin, delegates to crud.py

frontend/
├── src/
│   ├── api/projects.js      # fetch wrappers, one place all API calls live
│   ├── components/
│   │   ├── ProjectList.js
│   │   └── ProjectDetail.js
│   └── App.js
```

**Why separate `routes`, `crud`, and `schemas`:** each layer has one job.
Routes handle HTTP status codes and request parsing. `crud.py` only knows
about the database — it could be unit-tested with no HTTP layer involved at
all. `schemas.py` is the contract between frontend and backend, independent
of how data is stored. This is more structure than a single-file app needs,
but it's the structure a bigger version of this app would already need, so
it costs nothing to start with it.

**Progress calculation** (`crud.get_project_progress`) is real logic, not a
pass-through: it computes completion percentage from milestone status,
guarding against division by zero for projects with no milestones yet.

## Running locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
API runs at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

### Frontend
```bash
cd frontend
npm install
npm start
```
App runs at `http://localhost:3000`.

## What I'd add next

- Auth (JWT), so projects are scoped to a user
- Postgres for production persistence
- Tests for the `crud.py` layer (pure functions, easy to unit test)
- Deadline reminders / notifications as launch dates approach
