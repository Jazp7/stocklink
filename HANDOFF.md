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

## Tech Stack (FINAL — do not change without updating the Decisions/ folder)

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
│   │   │   ├── products.py
│   │   │   └── providers.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── products.py
│   │   │   └── providers.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── products.py
│   │   │   └── providers.py
│   │   ├── __init__.py
│   │   ├── database.py         ← EMPTY, needs to be written
│   │   └── main.py             ← EMPTY, needs to be written
│   ├── .env                    ← EMPTY, needs DATABASE_URL filled in
│   ├── .gitignore
│   ├── .python-version
│   ├── pyproject.toml
│   └── uv.lock
├── frontend/
│   ├── node_modules/
│   ├── public/
│   ├── src/                    ← default Vite files, not customized yet
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
├── Decisions/
└── README.md
```

> ⚠️ The extra `backend/main.py` (created by `uv init`) may still need to be deleted. The real one is at `backend/app/main.py`.

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

| Package        | Purpose                          |
|----------------|----------------------------------|
| fastapi        | Web framework, builds the API    |
| uvicorn        | Server that runs FastAPI         |
| asyncpg        | Connects Python to PostgreSQL    |
| python-dotenv  | Reads .env file                  |

---

## What Still Needs to Be Done

### Backend (next immediate step)

Write these files in order:

1. **`backend/.env`** — add the `DATABASE_URL` from Supabase
   ```
   DATABASE_URL=postgresql://postgres:your-password@db.your-project.supabase.co:5432/postgres
   SECRET_KEY=any_long_random_string
   ENV_MODE=development
   ```

2. **`backend/app/database.py`** — connection pool to Supabase using asyncpg

3. **`backend/app/schemas/providers.py`** — Pydantic models for providers (ProviderCreate, ProviderUpdate, ProviderResponse)

4. **`backend/app/schemas/products.py`** — Pydantic models for products (ProductCreate, ProductUpdate, ProductResponse)

5. **`backend/app/models/providers.py`** — SQL query functions for providers (get_all, get_one, create, update, delete)

6. **`backend/app/models/products.py`** — SQL query functions for products (get_all, get_one, create, update, delete)

7. **`backend/app/routers/providers.py`** — FastAPI route handlers for providers

8. **`backend/app/routers/products.py`** — FastAPI route handlers for products (with pagination, sorting, filtering, field selection)

9. **`backend/app/main.py`** — FastAPI app entry point, registers routers, sets up DB connection

### Frontend (not started yet)
- Needs `src/` folder restructured into `components/`, `pages/`, `services/`, `types/`
- Needs `frontend/.env` with `VITE_API_URL=http://127.0.0.1:8000`
- Full CRUD UI for products and providers

### Deployment (optional, do last)
- Backend → Render or Railway
- Frontend → Vercel
- Update README.md with live URLs

---

## API Response Format (MUST follow always)

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

## API Endpoints to Implement

| Method | Endpoint        | Description           |
|--------|-----------------|-----------------------|
| GET    | /products       | List all products     |
| GET    | /products/{id}  | Get single product    |
| POST   | /products       | Create product        |
| PUT    | /products/{id}  | Update product        |
| DELETE | /products/{id}  | Delete product        |
| GET    | /providers      | List all providers    |
| GET    | /providers/{id} | Get single provider   |
| POST   | /providers      | Create provider       |
| PUT    | /providers/{id} | Update provider       |
| DELETE | /providers/{id} | Delete provider       |

### Query parameters for GET list endpoints
- `page`, `limit` — pagination
- `sort` — e.g. `?sort=price` or `?sort=-price` (descending)
- `fields` — e.g. `?fields=id,name,price`
- `name`, `category`, `price[gte]`, `price[lte]` — filtering

---

## How to Run (once backend code is written)

```bash
# Backend
cd C:\Users\arist\Desktop\stocklink\backend
uv run uvicorn app.main:app --reload
# → runs at http://127.0.0.1:8000
# → auto docs at http://127.0.0.1:8000/docs

# Frontend
cd C:\Users\arist\Desktop\stocklink\frontend
pnpm dev
# → runs at http://localhost:5173
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

Full rationale + change implications in the `Decisions/` folder.

---

## Important Notes for AI Agents

- Always read `AGENTS.md` before writing or changing code
- Always check the `Decisions/` folder before refactoring
- Never use `float` for price — always `DECIMAL` / `Decimal`
- Never hardcode secrets — always use `.env`
- The student is a beginner — explain what code does, don't just write it
- Windows machine (PowerShell), VS Code, Python 3.13.7
