from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

# ProductBase: Common fields for all products.
# Note that we use Decimal for price as per the project's hard rules.
class ProductBase(BaseModel):
    name: str
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    stock_quantity: int = Field(..., ge=0) # ge=0 means it must be 0 or greater
    category: str
    description: Optional[str] = None
    provider_id: int

# ProductCreate: Used when adding a NEW product.
class ProductCreate(ProductBase):
    pass

# ProductUpdate: Used when updating an existing product.
# Everything is optional, but we still want price to be a Decimal if it's updated.
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

    # Again, this allows Pydantic to read from database rows.
    model_config = ConfigDict(from_attributes=True)

# ProductResponse: Success format for a single product.
class ProductResponse(BaseModel):
    success: bool = True
    data: Product

# ProductListResponse: Success format for a list of products.
class ProductListResponse(BaseModel):
    success: bool = True
    data: List[Product]
    # In the future, we can add 'pagination' here if needed.
