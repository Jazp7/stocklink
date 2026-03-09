# Decision 8 — CORS Configuration

**Decision:** Enable Cross-Origin Resource Sharing (CORS) in the FastAPI backend via `CORSMiddleware`.

**Why:**
- Browsers block scripts from making requests to a different domain/port than the one that served the page (security policy).
- Since the frontend runs on `localhost:5173` and the backend on `localhost:8000`, CORS must be explicitly allowed.
- We configured specific origins (`http://localhost:5173`) rather than using `*` (allow all) to maintain good security practices.

**Implications of removing CORS:**
- The frontend would be unable to fetch data, resulting in "CORS error" or "Network Error" in the browser console.
- The app would effectively be broken for browser-based users.
