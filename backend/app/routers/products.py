from fastapi import APIRouter, Depends, HTTPException, status
import asyncpg
from typing import List
from ..database import get_db_connection
from ..models import products as products_model
from ..schemas.products import (
    Product, 
    ProductCreate, 
    ProductUpdate, 
    ProductResponse, 
    ProductListResponse
)

# We group all /products endpoints together.
router = APIRouter(prefix="/products", tags=["Products"])

# GET /products: List all products.
@router.get("/", response_model=ProductListResponse)
async def list_products(conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch all products from the database."""
    records = await products_model.get_all(conn)
    return {"success": True, "data": records}

# GET /products/{product_id}: Get details for one product.
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Fetch a single product by ID."""
    record = await products_model.get_by_id(conn, product_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Product with ID {product_id} not found."
                }
            }
        )
    return {"success": True, "data": record}

# POST /products: Create a new product.
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Add a new product to the database."""
    try:
        # We try to create the product.
        record = await products_model.create(conn, product)
        return {"success": True, "data": record}
    except asyncpg.exceptions.ForeignKeyViolationError:
        # If the provider_id doesn't exist in our 'providers' table, 
        # the database will reject the insert and throw this error.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_PROVIDER",
                    "message": f"Provider with ID {product.provider_id} does not exist."
                }
            }
        )

# PUT /products/{product_id}: Update a product.
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int, 
    product: ProductUpdate, 
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Update an existing product's info."""
    try:
        record = await products_model.update(conn, product_id, product)
        if not record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Product with ID {product_id} not found."
                    }
                }
            )
        return {"success": True, "data": record}
    except asyncpg.exceptions.ForeignKeyViolationError:
        # Also handle potential provider updates that point to non-existent providers.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "INVALID_PROVIDER",
                    "message": f"Provider with ID {product.provider_id} does not exist."
                }
            }
        )

# DELETE /products/{product_id}: Remove a product.
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Delete a product by ID."""
    success = await products_model.delete(conn, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Product with ID {product_id} not found."
                }
            }
        )
    return {"success": True, "data": None}
