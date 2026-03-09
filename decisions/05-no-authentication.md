# Decision 5 — No Authentication

**Decision:** The application has no login system, user accounts, or access control.

**Why:**
- Not required by the technical assessment.
- Adding auth (JWT, OAuth, sessions) would significantly increase complexity.
- RLS (Row Level Security) in Supabase is disabled for the same reason.

**Implications of adding authentication later:**
- A `users` table would need to be added to the database.
- FastAPI would need JWT middleware (e.g. `python-jose` or `fastapi-users`).
- All protected endpoints would need a `Depends(get_current_user)` dependency.
- Frontend would need login/register pages and token storage logic.
- Supabase RLS policies would need to be written per table.
