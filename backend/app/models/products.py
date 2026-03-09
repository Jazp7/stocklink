import asyncpg
from typing import List, Optional
from ..schemas.products import ProductCreate, ProductUpdate

# Fetch all products from the database.
async def get_all(conn: asyncpg.Connection) -> List[asyncpg.Record]:
    """Fetch all products, showing newest ones first."""
    # Simple query for now, but we'll add filtering later.
    return await conn.fetch("SELECT * FROM products ORDER BY created_at DESC")

# Fetch a single product by its unique ID.
async def get_by_id(conn: asyncpg.Connection, product_id: int) -> Optional[asyncpg.Record]:
    """Fetch a single product by ID."""
    return await conn.fetchrow("SELECT * FROM products WHERE id = $1", product_id)

# Create a new product.
async def create(conn: asyncpg.Connection, product: ProductCreate) -> asyncpg.Record:
    """Insert a new product and return the record."""
    # This query matches the 'products' table schema.
    # provider_id connects this product to a specific provider.
    query = """
        INSERT INTO products (name, price, stock_quantity, category, description, provider_id)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING *
    """
    return await conn.fetchrow(
        query, 
        product.name, 
        product.price, 
        product.stock_quantity, 
        product.category, 
        product.description, 
        product.provider_id
    )

# Update an existing product's fields.
async def update(conn: asyncpg.Connection, product_id: int, product: ProductUpdate) -> Optional[asyncpg.Record]:
    """Update fields of an existing product."""
    # Just like with providers, we only want to update fields 
    # that the user actually sent us.
    update_data = product.model_dump(exclude_unset=True)
    if not update_data:
        return await get_by_id(conn, product_id)

    set_clause = []
    values = []
    for i, (key, value) in enumerate(update_data.items(), start=1):
        set_clause.append(f"{key} = ${i}")
        values.append(value)
    
    values.append(product_id)
    query = f"""
        UPDATE products 
        SET {', '.join(set_clause)}, updated_at = NOW() 
        WHERE id = ${len(values)} 
        RETURNING *
    """
    
    return await conn.fetchrow(query, *values)

# Remove a product from the database.
async def delete(conn: asyncpg.Connection, product_id: int) -> bool:
    """Delete a product by ID and return True if successful."""
    result = await conn.execute("DELETE FROM products WHERE id = $1", product_id)
    return result == "DELETE 1"
