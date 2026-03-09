import asyncpg
from typing import List, Optional
from ..schemas.providers import ProviderCreate, ProviderUpdate

# Get all providers from the database.
async def get_all(conn: asyncpg.Connection) -> List[asyncpg.Record]:
    """Fetch all providers from the database."""
    # We use a simple SELECT query.
    return await conn.fetch("SELECT * FROM providers ORDER BY created_at DESC")

# Get a single provider by their unique ID.
async def get_by_id(conn: asyncpg.Connection, provider_id: int) -> Optional[asyncpg.Record]:
    """Fetch a single provider by ID."""
    # fetchrow() is used when we only expect ONE result.
    return await conn.fetchrow("SELECT * FROM providers WHERE id = $1", provider_id)

# Add a new provider.
async def create(conn: asyncpg.Connection, provider: ProviderCreate) -> asyncpg.Record:
    """Insert a new provider into the database and return the full record."""
    # We use RETURNING * so the database sends back the final row, 
    # including the ID it just generated.
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
    # This one is a bit trickier because we only want to update fields 
    # that are actually provided in the request.
    
    # We get all the data from our Pydantic schema as a dictionary.
    # exclude_unset=True means we only get fields the user actually sent.
    update_data = provider.model_dump(exclude_unset=True)
    if not update_data:
        # If no data was provided, just return the existing record.
        return await get_by_id(conn, provider_id)

    # Build the SQL query dynamically based on which fields were provided.
    set_clause = []
    values = []
    for i, (key, value) in enumerate(update_data.items(), start=1):
        set_clause.append(f"{key} = ${i}")
        values.append(value)
    
    # Add the provider_id as the last parameter for the WHERE clause.
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
    # execute() just runs the command and returns the result string.
    result = await conn.execute("DELETE FROM providers WHERE id = $1", provider_id)
    # result looks like "DELETE 1" if one row was deleted.
    return result == "DELETE 1"
