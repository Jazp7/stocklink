from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ProductBase: Common fields for all products.
class ProductBase(BaseModel):
    name: str
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    stock_quantity: int = Field(..., ge=0)
    category: str
    description: Optional[str] = None
    # We make this Optional[int] so products without a provider don't crash the API.
    provider_id: Optional[int] = None

# ProductCreate: Used when adding a NEW product.
class ProductCreate(ProductBase):
    pass

# ProductUpdate: Used when updating an existing product.
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = Field(None, max_digits=10, decimal_places=2)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    description: Optional[str] = None
    provider_id: Optional[int] = None

# Product: The complete product as it appears in the database.
class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ProductResponse: Success format for a single product.
class ProductResponse(BaseModel):
    success: bool = True
    data: Product

from .api import PaginationInfo

# ProductListResponse: Success format for a list of products.
class ProductListResponse(BaseModel):
    success: bool = True
    data: List[Product]
    pagination: Optional[PaginationInfo] = None
