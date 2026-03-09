# AGENTS.md — AI Coding Assistant Instructions

This file contains instructions for any AI agent (Gemini, Claude, Copilot, etc.) working on this project. Read this file **before** writing, editing, or refactoring any code.

---

## Project Summary

**Stocklink** is a full-stack product and provider management system. It exposes a RESTful API and a React frontend to perform full CRUD operations on two related resources: `products` and `providers`.

---

## Rules for AI Agents

1. **Always check the `decisions/` folder before refactoring.**
2. **Never change the folder structure** without updating `README.md` and `HANDOFF.md`.
3. **Never add authentication.** This project intentionally has no auth.
4. **Always validate on both sides.** Backend uses Pydantic schemas. Frontend validates before sending requests.
5. **Never use `float` for money.** The `price` field is always `DECIMAL(10,2)` in the DB and `Decimal` in Python.
6. **Always return consistent JSON.** Success responses use `{ "success": true, "data": ... }`. 
7. **Type Safety**: Use `export type` and `import type` for all TypeScript definitions to ensure compatibility with Vite.

---

## API Endpoints Reference

| Method | Endpoint           | Description              | Parameters |
|--------|--------------------|--------------------------|------------|
| GET    | /products/         | List all products        | `page`, `limit` |
| GET    | /products/{id}     | Get single product       | |
| POST   | /products/         | Create new product       | |
| PUT    | /products/{id}     | Update existing product  | |
| DELETE | /products/{id}     | Delete product           | |
| GET    | /providers/        | List all providers       | `page`, `limit` |
| GET    | /providers/{id}    | Get single provider      | |
| POST   | /providers/        | Create new provider      | |
| PUT    | /providers/{id}    | Update existing provider | |
| DELETE | /providers/{id}    | Delete provider          | |
| GET    | /dashboard/stats/  | Get summary statistics   | |

---

## Files Written So Far

| File | Status |
|------|--------|
| `backend/app/database.py` | ✓ Done |
| `backend/app/schemas/` | ✓ Done (products, providers, api) |
| `backend/app/models/` | ✓ Done (products, providers, dashboard) |
| `backend/app/routers/` | ✓ Done (products, providers, dashboard) |
| `backend/app/main.py` | ✓ Done (CORS included) |
| `frontend/src/` | ✓ 100% Functional |
| `backend/db_seeder_reference.py` | ✓ Reference tool |
