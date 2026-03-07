# AGENTS.md — AI Coding Assistant Instructions

This file contains instructions for any AI agent (Gemini, Claude, Copilot, etc.) working on this project. Read this file **before** writing, editing, or refactoring any code.

---

## Project Summary

**Stocklink** is a full-stack product and provider management system built as a technical assessment. It exposes a RESTful API and a React frontend to perform full CRUD operations on two related resources: `products` and `providers`.

---

## Rules for AI Agents

1. **Always check the `Decisions/` folder before refactoring.** If you change a technology, a pattern, or a structural decision, document why in the `Decisions/` folder.
2. **Never change the folder structure** without updating section 6 of the Notion notes and `README.md`.
3. **Never add authentication or user login.** This project intentionally has no auth.
4. **Always validate on both sides.** Backend uses Pydantic schemas. Frontend validates before sending requests.
5. **Never use `float` for money.** The `price` field is always `DECIMAL(10,2)` in the DB and `Decimal` in Python.
6. **Always return consistent JSON.** Success responses use `{ "success": true, "data": ... }`. Error responses use `{ "success": false, "error": { "code": ..., "message": ..., "details": ... } }`.
7. **Do not install unnecessary packages.** Check `pyproject.toml` and `package.json` before adding a new dependency.
8. **Environment variables are never hardcoded.** All secrets and URLs come from `.env` files.

---

## Tech Stack (Do Not Change Without Updating the Decisions/ Folder)

| Layer      | Technology              |
|------------|-------------------------|
| Frontend   | React + TypeScript, Vite, pnpm |
| Backend    | Python, FastAPI, uv     |
| Database   | PostgreSQL via Supabase  |
| Testing    | Vitest (frontend), Postman (API) |

---

## Folder Structure

```
stocklink/
├── frontend/           # React + TypeScript (Vite)
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── pages/      # One file per view
│   │   ├── services/   # API call functions
│   │   └── types/      # TypeScript type definitions
├── backend/            # Python + FastAPI
│   ├── app/
│   │   ├── routers/    # One file per resource (products, providers)
│   │   ├── models/     # Database query logic
│   │   └── schemas/    # Pydantic models / validation
├── AGENTS.md
├── Decisions/            # Architecture Decision Records
└── README.md
```

---

## API Response Format

Always follow this structure:

```json
// Success
{
  "success": true,
  "data": { ... }
}

// Success with pagination
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

## API Endpoints Reference

| Method | Endpoint           | Description              |
|--------|--------------------|--------------------------|
| GET    | /products          | List all products        |
| GET    | /products/:id      | Get single product       |
| POST   | /products          | Create product           |
| PUT    | /products/:id      | Update product           |
| DELETE | /products/:id      | Delete product           |
| GET    | /providers         | List all providers       |
| GET    | /providers/:id     | Get single provider      |
| POST   | /providers         | Create provider          |
| PUT    | /providers/:id     | Update provider          |
| DELETE | /providers/:id     | Delete provider          |

### Supported Query Parameters (GET list endpoints)
- `page`, `limit` — pagination
- `sort` — sorting (e.g. `sort=price`, `sort=-price` for descending)
- `fields` — field selection (e.g. `fields=id,name,price`)
- `name`, `category`, `price[gte]`, `price[lte]` — filtering

---

## Database Schema Summary

```sql
providers (id, name, email, address, phone, description, created_at, updated_at)
products  (id, name, price, stock_quantity, category, description, provider_id → providers.id, created_at, updated_at)
```

Relationship: One provider → Many products (One-to-Many). `provider_id` is a Foreign Key in `products`.
