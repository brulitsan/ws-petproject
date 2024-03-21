from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field
from ws_src.common.choices import BaseOrderStatus
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
    quantity: Optional[Decimal] = None
    type: str
    status: str = BaseOrderStatus.in_process

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True

    def update_quantity(self) -> None:
        product_price = self.product.last_price
        quantity = self.transaction_price / product_price
        self.quantity = quantity


class AutoOperationsOrderSchema(OrderSchema):
    currency_price: Decimal
