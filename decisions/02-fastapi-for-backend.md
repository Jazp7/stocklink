# Decision 2 — FastAPI (Python) for the Backend

**Decision:** Use FastAPI as the backend framework.

**Why:**
- Python was the chosen backend language.
- FastAPI automatically generates interactive API documentation at `/docs` (Swagger UI) — useful for testing without Postman.
- Built-in request validation via Pydantic schemas.
- Very beginner-friendly: routes are just Python functions.
- Strong community and documentation.

**Implications of changing to Flask or Django:**
- Flask: Less built-in validation, no auto-docs, more manual setup required.
- Django: Much heavier framework, overkill for a simple REST API, steep learning curve.
- Pydantic schemas would need to be replaced or adapted.
