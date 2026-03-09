# Decision 3 — Supabase for the Database

**Decision:** Use Supabase as the hosted PostgreSQL database provider.

**Why:**
- Free tier is sufficient for this project.
- Provides a visual Table Editor (no need for local PostgreSQL setup).
- Provides a direct PostgreSQL connection string — backend connects to it like any standard Postgres DB.
- No need to manage database infrastructure locally.

**Implications of changing to local PostgreSQL:**
- `DATABASE_URL` in `.env` would point to `localhost` instead of Supabase.
- Developers would need PostgreSQL installed locally to run the project.
- The SQL schema (`CREATE TABLE` statements) remains the same — no query changes needed.
