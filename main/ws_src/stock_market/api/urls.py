from django.urls import path

from .views import BuyItemViewSet, StockMarketViewSet

urlpatterns = [
    path("get_coins/", StockMarketViewSet.as_view({"get": "list"})),
    path("buy_coins/", BuyItemViewSet.as_view({"post": "create"})),
]
