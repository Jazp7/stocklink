import asyncpg
from decimal import Decimal

async def get_stats(conn: asyncpg.Connection):
    """Calculate summary statistics for the dashboard."""
    
    # 1. Total counts
    total_products = await conn.fetchval("SELECT COUNT(*) FROM products")
    total_providers = await conn.fetchval("SELECT COUNT(*) FROM providers")
    
    # 2. Total stock value (Price * Quantity for all items)
    # We use COALESCE to handle the case where there are no products (returns 0 instead of None)
    total_value = await conn.fetchval("SELECT COALESCE(SUM(price * stock_quantity), 0) FROM products")
    
    # 3. Out of stock count
    out_of_stock = await conn.fetchval("SELECT COUNT(*) FROM products WHERE stock_quantity = 0")
    
    # 4. Low stock count (e.g. less than 10 units)
    low_stock = await conn.fetchval("SELECT COUNT(*) FROM products WHERE stock_quantity > 0 AND stock_quantity < 10")

    return {
        "total_products": total_products,
        "total_providers": total_providers,
        "total_value": Decimal(str(total_value)),
        "out_of_stock": out_of_stock,
        "low_stock": low_stock
    }
