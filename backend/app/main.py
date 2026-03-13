import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import db
from .routers import providers, products, dashboard # Added dashboard
from dotenv import load_dotenv

# This @asynccontextmanager handles the life cycle of the app.
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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://stocklink-nine.vercel.app",
        "http://stocklink-nine.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our routers. 
app.include_router(providers.router)
app.include_router(products.router)
app.include_router(dashboard.router) # Added dashboard

# A simple "Health Check" endpoint.
@app.get("/")
async def root():
    return {
        "success": True, 
        "message": "Welcome to the Stocklink API! Go to /docs for the documentation."
    }
