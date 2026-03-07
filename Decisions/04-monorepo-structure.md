# Decision 4 — Monorepo Structure

**Decision:** Both `frontend/` and `backend/` live inside a single `stocklink/` Git repository.

**Why:**
- Easier to manage as a solo developer — one repo, one clone, one place to look.
- Shared documentation files (`AGENTS.md`, `DECISIONS.md`, `README.md`) sit at the root and apply to both sides.
- Avoids the overhead of coordinating two separate repositories.

**Implications of splitting into two repos:**
- `README.md`, `AGENTS.md`, and `DECISIONS.md` would need to be duplicated or split.
- Deployment configurations would need to reference separate repos.
- Contributors would need to clone and manage two repositories.
