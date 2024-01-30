import uuid

from pydantic import BaseModel, Field

from ws_src.users.models import User


class StockMarketBuy(BaseModel):
    product_id: str
    purchase_amount: float
    order_type: str


class StockMarketSell(BaseModel):
    product_id: str
    sale_amount: float
    order_type: str


class ProductModel(BaseModel):
    id: str = Field(alias='_id')
    symbol: str
    highPrice: float
    lowPrice: float
    lastPrice: float


class OrderDto(BaseModel):
    user: User
    product_id: str
    transaction_price: float
    quantity: float
    type: str

    class Config:
        arbitrary_types_allowed = True
