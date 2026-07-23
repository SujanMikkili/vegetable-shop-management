"""
Pydantic schemas for request validation.
These mirror exactly the JSON bodies the existing frontend already sends,
so no frontend changes are required.
"""

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    unit: str
    original_price: float
    selling_price: float
    quantity: float


class StockUpdate(BaseModel):
    item_id: int
    quantity: float


class PriceUpdate(BaseModel):
    id: int
    original_price: float
    selling_price: float


class CartAdd(BaseModel):
    item_id: int
    quantity: float
    unit: str


class CartRemove(BaseModel):
    cart_id: int
