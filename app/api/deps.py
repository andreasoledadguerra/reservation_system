# This file centralizes reusable dependencies. It re‑exports the get_db generator to avoid circular imports to keep the endpoint files clean.
from app.core.database import get_db