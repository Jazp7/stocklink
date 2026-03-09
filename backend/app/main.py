from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database import db
from .routers import providers, products

# This @asynccontextmanager handles the life cycle of the app.
# It runs when the app starts and when it stops.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Connect to the database pool.
    print("Connecting to the database...")
    await db.connect()
    yield
    # SHUTDOWN: Close the database pool.
    print("Closing database connection...")
    await db.disconnect()

# Create the main FastAPI app.
app = FastAPI(
    title="Stocklink API",
    description="A simple API to manage products and providers.",
    version="1.0.0",
    lifespan=lifespan
)

# Include our routers. 
# This tells FastAPI to use the endpoints we defined in those files.
app.include_router(providers.router)
app.include_router(products.router)

# A simple "Health Check" endpoint.
@app.get("/")
async def root():
    return {
        "success": True, 
        "message": "Welcome to the Stocklink API! Go to /docs for the documentation."
    }
