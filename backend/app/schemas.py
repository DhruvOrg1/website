"""Pydantic schemas: request validation and response serialization."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --------------------------------------------------------------------------- #
# Category
# --------------------------------------------------------------------------- #
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None


class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


# --------------------------------------------------------------------------- #
# Product
# --------------------------------------------------------------------------- #
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    sku: str = Field(..., min_length=1, max_length=64)
    description: str | None = None
    price: float = Field(0, ge=0)
    quantity: int = Field(0, ge=0)
    low_stock_threshold: int = Field(0, ge=0)
    category_id: int | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    sku: str | None = Field(None, min_length=1, max_length=64)
    description: str | None = None
    price: float | None = Field(None, ge=0)
    quantity: int | None = Field(None, ge=0)
    low_stock_threshold: int | None = Field(None, ge=0)
    category_id: int | None = None


class StockAdjustment(BaseModel):
    """Relative change to stock: positive to restock, negative to sell/remove."""

    delta: int = Field(..., description="Amount to add (+) or remove (-).")
    reason: str | None = Field(None, max_length=255)


class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_low_stock: bool
    created_at: datetime
    updated_at: datetime


# --------------------------------------------------------------------------- #
# Auth / User
# --------------------------------------------------------------------------- #
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
