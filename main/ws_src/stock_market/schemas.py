from decimal import Decimal

from pydantic import BaseModel, Field
from ws_src.stock_market.models import Product
from ws_src.users.models import User


class ProductSchema(BaseModel):
    symbol: str
    last_price: Decimal = Field(alias="lastPrice")
    high_price: Decimal = Field(alias="highPrice")
    low_price: Decimal = Field(alias="lowPrice")


class OrderSchema(BaseModel):
    user: User
    product: Product
    transaction_price: Decimal
    quantity: Decimal
    type: str

    class Config:
        arbitrary_types_allowed = True
