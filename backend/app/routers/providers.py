from fastapi import APIRouter, Depends, HTTPException, status, Query
import asyncpg
import math
from typing import List
from ..database import get_db_connection
from ..models import providers as providers_model
from ..schemas.providers import (
    Provider, 
    ProviderCreate, 
    ProviderUpdate, 
    ProviderResponse, 
    ProviderListResponse
)
from ..schemas.api import PaginationInfo

# We create an APIRouter to group all /providers endpoints.
router = APIRouter(prefix="/providers", tags=["Providers"])

# GET /providers: List all providers with pagination.
@router.get("/", response_model=ProviderListResponse)
async def list_providers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Fetch all providers from the database with pagination."""
    offset = (page - 1) * limit

    # Get the data and the total count
    records = await providers_model.get_all(conn, limit, offset)
    total_items = await providers_model.get_total_count(conn)
    
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 0

    return {
        "success": True, 
        "data": [dict(r) for r in records],
        "pagination": {
            "page": page,
            "limit": limit,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }

# GET /providers/{provider_id}: Get details for one provider.
@router.get("/{provider_id}", response_model=ProviderResponse)
async def get_provider(provider_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch a single provider by ID."""
    record = await providers_model.get_by_id(conn, provider_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Provider with ID {provider_id} not found."
                }
            }
        )
    return {"success": True, "data": dict(record)}

# POST /providers: Create a new provider.
@router.post("/", response_model=ProviderResponse, status_code=status.HTTP_201_CREATED)
async def create_provider(provider: ProviderCreate, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Add a new provider to the database."""
    record = await providers_model.create(conn, provider)
    return {"success": True, "data": dict(record)}

# PUT /providers/{provider_id}: Update an existing provider.
@router.put("/{provider_id}", response_model=ProviderResponse)
async def update_provider(
    provider_id: int, 
    provider: ProviderUpdate, 
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Update an existing provider's info."""
    record = await providers_model.update(conn, provider_id, provider)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Provider with ID {provider_id} not found."
                }
            }
        )
    return {"success": True, "data": dict(record)}

# DELETE /providers/{provider_id}: Remove a provider.
@router.delete("/{provider_id}", status_code=status.HTTP_200_OK)
async def delete_provider(provider_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Delete a provider by ID and return True if successful."""
    success = await providers_model.delete(conn, provider_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Provider with ID {provider_id} not found."
                }
            }
        )
    return {"success": True, "data": None}
