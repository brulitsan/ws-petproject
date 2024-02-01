from decimal import Decimal

from pydantic import BaseModel, Field

from ws_src.stock_market.models import Product
from ws_src.users.models import User


class ProductSchema(BaseModel):
    id: str = Field(alias="_id")
    symbol: str
    lastPrice: Decimal
    highPrice: Decimal
    lowPrice: Decimal


class OrderSchema(BaseModel):
    user: User
    product: Product
    transaction_price: Decimal
    quantity: Decimal
    type: str

    class Config:
        arbitrary_types_allowed = True
