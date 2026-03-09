import asyncpg
from typing import List, Optional
from ..schemas.providers import ProviderCreate, ProviderUpdate

# Get all providers from the database with pagination.
async def get_all(conn: asyncpg.Connection, limit: int = 10, offset: int = 0) -> List[asyncpg.Record]:
    """Fetch all providers from the database with pagination."""
    query = "SELECT * FROM providers ORDER BY created_at ASC LIMIT $1 OFFSET $2"
    return await conn.fetch(query, limit, offset)

# Get the total number of providers for pagination.
async def get_total_count(conn: asyncpg.Connection) -> int:
    """Return the total number of providers in the database."""
    count = await conn.fetchval("SELECT COUNT(*) FROM providers")
    return count

# Get a single provider by their unique ID.
async def get_by_id(conn: asyncpg.Connection, provider_id: int) -> Optional[asyncpg.Record]:
    """Fetch a single provider by ID."""
    return await conn.fetchrow("SELECT * FROM providers WHERE id = $1", provider_id)

# Add a new provider.
async def create(conn: asyncpg.Connection, provider: ProviderCreate) -> asyncpg.Record:
    """Insert a new provider into the database and return the full record."""
    query = """
        INSERT INTO providers (name, email, address, phone, description)
        VALUES ($1, $2, $3, $4, $5)
        RETURNING *
    """
    return await conn.fetchrow(
        query, 
        provider.name, 
        provider.email, 
        provider.address, 
        provider.phone, 
        provider.description
    )

# Update an existing provider.
async def update(conn: asyncpg.Connection, provider_id: int, provider: ProviderUpdate) -> Optional[asyncpg.Record]:
    """Update fields of an existing provider."""
    update_data = provider.model_dump(exclude_unset=True)
    if not update_data:
        return await get_by_id(conn, provider_id)

    set_clause = []
    values = []
    for i, (key, value) in enumerate(update_data.items(), start=1):
        set_clause.append(f"{key} = ${i}")
        values.append(value)
    
    values.append(provider_id)
    query = f"""
        UPDATE providers 
        SET {', '.join(set_clause)}, updated_at = NOW() 
        WHERE id = ${len(values)} 
        RETURNING *
    """
    
    return await conn.fetchrow(query, *values)

# Remove a provider.
async def delete(conn: asyncpg.Connection, provider_id: int) -> bool:
    """Delete a provider by ID and return True if successful."""
    result = await conn.execute("DELETE FROM providers WHERE id = $1", provider_id)
    return result == "DELETE 1"
