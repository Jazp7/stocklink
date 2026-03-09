from fastapi import APIRouter, Depends, HTTPException, status, Query
import asyncpg
import math
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
from ..schemas.api import PaginationInfo

# We group all /products endpoints together.
router = APIRouter(prefix="/products", tags=["Products"])

# GET /products: List all products with pagination.
@router.get("/", response_model=ProductListResponse)
async def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    conn: asyncpg.Connection = Depends(get_db_connection)
):
    """Fetch all products from the database with pagination."""
    try:
        offset = (page - 1) * limit
        
        # Get the data and the total count
        records = await products_model.get_all(conn, limit, offset)
        total_items = await products_model.get_total_count(conn)
        
        total_pages = math.ceil(total_items / limit) if total_items > 0 else 0
        
        # Convert asyncpg.Record to dict. FastAPI/Pydantic will handle the Decimal conversion.
        data = [dict(r) for r in records]
        
        return {
            "success": True, 
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_items": total_items,
                "total_pages": total_pages
            }
        }
    except Exception as e:
        print(f"Error in list_products: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

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
    return {"success": True, "data": dict(record)}

# POST /products: Create a new product.
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate, conn: asyncpg.Connection = Depends(get_db_connection)):
    """Add a new product to the database."""
    try:
        record = await products_model.create(conn, product)
        return {"success": True, "data": dict(record)}
    except asyncpg.exceptions.ForeignKeyViolationError:
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
        return {"success": True, "data": dict(record)}
    except asyncpg.exceptions.ForeignKeyViolationError:
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
    """Delete a product by ID and return True if successful."""
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
