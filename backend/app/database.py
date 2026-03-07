import os
import asyncpg
from dotenv import load_dotenv

# Load environment variables from the .env file in the backend directory
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

class Database:
    def __init__(self):
        self.pool = None

    async def connect(self):
        """Create a connection pool to the Supabase PostgreSQL database."""
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set. Please check your .env file.")
        
        # Create a connection pool that will hold a set of active connections
        self.pool = await asyncpg.create_pool(dsn=DATABASE_URL)

    async def disconnect(self):
        """Close all connections in the pool."""
        if self.pool:
            await self.pool.close()

# Create a global singleton instance to be used across the application
db = Database()

# FastAPI dependency to get a single connection from the pool for a request
async def get_db_connection():
    if not db.pool:
        raise RuntimeError("Database pool is not initialized. Ensure db.connect() is called on app startup.")
    
    async with db.pool.acquire() as connection:
        yield connection
