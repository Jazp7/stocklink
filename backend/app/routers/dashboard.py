from fastapi import APIRouter, Depends
import asyncpg
from ..database import get_db_connection
from ..models import dashboard as dashboard_model

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch summary statistics for the dashboard."""
    stats = await dashboard_model.get_stats(conn)
    return {
        "success": True,
        "data": stats
    }
