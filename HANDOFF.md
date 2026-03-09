# HANDOFF.md — Stocklink Project Handoff & Progress Summary

This document is a full summary of everything decided and done so far in the Stocklink project. Share this with any AI assistant (or a new conversation) to resume work without losing context.

---

## What is this project?

**Stocklink** is a full-stack product and provider management system built as a technical assessment for a university dev community. The goal is to pass a test to become a "Developer" (instead of "Apprentice/Learner").

The developer is a **2nd year software engineering student** with:
- Some React experience (frontend only)
- No backend experience
- No database experience
- No deployment experience

Everything is AI-assisted. That is expected and acceptable.

---

## Tech Stack (FINAL — do not change without updating the decisions/ folder)

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React + TypeScript, Vite, pnpm      |
| Backend  | Python, FastAPI, uv                 |
| Database | PostgreSQL via Supabase              |
| Testing  | Vitest (frontend), Postman (API)    |

---

## Project Name

**Stocklink** — chosen for being technical and clean. Concept: products *linked* to their providers.

---

## Folder Structure (CURRENT STATE — verified working)

```
C:\Users\arist\Desktop\stocklink\
├── backend/
│   ├── .venv/                  ← created automatically by uv
│   ├── app/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── products.py     ← ✓ DONE
│   │   │   └── providers.py    ← ✓ DONE
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── products.py     ← ✓ DONE
│   │   │   └── providers.py    ← ✓ DONE
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── products.py     ← ✓ DONE
│   │   │   └── providers.py    ← ✓ DONE
│   │   ├── __init__.py
│   │   ├── database.py         ← ✓ DONE
│   │   └── main.py             ← ✓ DONE
│   ├── .env                    ← ✓ DATABASE_URL filled in
│   ├── .gitignore
│   ├── .python-version
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── components/         ← ✓ DONE (Layout)
│   │   ├── pages/              ← ✓ DONE (Placeholders: Dashboard, Products, Providers)
│   │   ├── services/           ← ✓ DONE (API calls)
│   │   ├── types/              ← ✓ DONE (TypeScript definitions)
│   │   ├── App.tsx             ← ✓ DONE (Routing)
│   │   └── main.tsx            ← ✓ DONE
│   ├── .env                    ← ✓ VITE_API_URL filled in
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
├── .gitignore
├── AGENTS.md
├── HANDOFF.md
├── decisions/                  ← folder with one .md file per decision
└── README.md
```

---

## Database (DONE ✓)

- Hosted on **Supabase** (free tier)
- Project name in Supabase: **Stocklink** (Jazp Organization)
- Both tables created and verified in the Table Editor
- RLS (Row Level Security) is **intentionally disabled** — no auth in this project

### SQL Schema

```sql
CREATE TABLE providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL,
    category VARCHAR(50),
    description TEXT,
    provider_id INTEGER REFERENCES providers(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Relationship
One-to-Many: one provider → many products. `provider_id` is the foreign key in `products`.

---

## Backend Dependencies (INSTALLED ✓)

Installed via `uv add` inside `backend/`:

| Package           | Purpose                            |
|-------------------|------------------------------------|
| fastapi           | Web framework, builds the API      |
| uvicorn           | Server that runs FastAPI           |
| asyncpg           | Connects Python to PostgreSQL      |
| python-dotenv     | Reads .env file                    |
| email-validator   | Required by Pydantic for EmailStr  |
| pydantic-settings | Handles .env and app settings      |

---

## What Has Been Written

### `backend/app/database.py` ✓
Creates a connection pool to Supabase using asyncpg.

### `backend/app/schemas/` ✓
Pydantic models for `providers` and `products` (Create, Update, and Response formats).

### `backend/app/models/` ✓
SQL query functions for both resources (get_all, get_by_id, create, update, delete).

### `backend/app/routers/` ✓
FastAPI route handlers that connect the schemas and models to HTTP endpoints.

### `backend/app/main.py` ✓
Entry point: creates the app, handles database connection life cycle, and registers routers.

### `frontend/src/` ✓
- **Layout**: Shared navigation and structure.
- **Routing**: React Router configured in `App.tsx`.
- **Services**: `productService.ts` and `providerService.ts` ready for API calls.
- **Types**: Full TypeScript interfaces for API responses and data models.
- **Pages**: Initial structure for Dashboard, Products, and Providers.

---

## What Still Needs to Be Done

### Frontend (DONE ✓)
- **Scaffolding**: Complete folder structure.
- **Routing**: Full React Router configuration.
- **Services**: All API calls for Products and Providers.
- **CRUD Logic**: Create, Read, Update, and Delete implemented for all resources.
- **UI/UX**: Clean layout with Sidebar, Tables, Modals, and consistent styling.
- **Type Safety**: Full TypeScript integration with `export type` and `import type`.

### Deployment (optional, do last)
- Backend → Render or Railway
- Frontend → Vercel
- Update README.md with live URLs

---

## How the Backend Files Connect

```
main.py
  → on startup: calls db.connect()
  → registers: routers/products.py and routers/providers.py

routers/products.py
  → receives HTTP request (e.g. GET /products)
  → calls a function from models/products.py
  → passes db connection from database.py

models/products.py
  → runs raw SQL against Supabase via asyncpg connection
  → returns data to the router

schemas/products.py
  → Pydantic models that validate request bodies and shape responses
  → used by routers to auto-validate incoming JSON
```

---

## How to Run (once backend code is written)

```bash
# Backend
cd C:\Users\arist\Desktop\stocklink\backend
uv run uvicorn app.main:app --reload
# → http://127.0.0.1:8000
# → interactive docs at http://127.0.0.1:8000/docs

# Frontend
cd C:\Users\arist\Desktop\stocklink\frontend
pnpm dev
# → http://localhost:5173
```

---

## API Response Format (MUST always follow)

```json
// Success (single item)
{ "success": true, "data": { ... } }

// Success (list with pagination)
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total_items": 50,
    "total_pages": 5
  }
}

// Error
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Product not found",
    "details": []
  }
}
```

---

## Key Decisions Summary

| Decision | Choice | Why |
|---|---|---|
| DB relationship | One-to-Many | Simpler, avoids junction table |
| Backend framework | FastAPI | Auto docs, Pydantic validation, beginner friendly |
| DB provider | Supabase | Free, visual editor, managed Postgres |
| Structure | Monorepo | One repo, easier for solo dev |
| Auth | None | Not required by assessment |
| Python pkg manager | uv | Fast, handles venv automatically |

Full rationale + change implications in the `decisions/` folder.

---

## Important Notes for AI Agents

- Always read `AGENTS.md` before writing or changing code
- Always check the `decisions/` folder before refactoring
- Never use `float` for price — always `DECIMAL` / `Decimal`
- Never hardcode secrets — always use `.env`
- The student is a beginner — explain what code does, don't just write it
- Windows machine (PowerShell), VS Code, Python 3.13.7