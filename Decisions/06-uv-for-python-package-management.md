# Decision 6 — uv for Python Package Management

**Decision:** Use `uv` instead of `pip` or `poetry` to manage Python dependencies.

**Why:**
- Significantly faster than pip.
- Handles virtual environments automatically.
- `uv sync` installs everything from `pyproject.toml` in one command — easy for anyone cloning the project.
- Modern tooling recommended for new Python projects.

**Implications of switching to pip:**
- `pyproject.toml` would be replaced by `requirements.txt`.
- Developers would need to manually create and activate a virtual environment.
- `uv sync` in setup instructions would become `pip install -r requirements.txt`.
