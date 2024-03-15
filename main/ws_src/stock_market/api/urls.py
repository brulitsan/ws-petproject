from django.urls import path

from .views import BuyItemViewSet, GetCurrencyInfo, StockMarketViewSet

urlpatterns = [
    path("get_coins/", StockMarketViewSet.as_view({"get": "list"})),
    path("buy_coins/", BuyItemViewSet.as_view({"post": "create"})),
    path("get_coins_info/", GetCurrencyInfo.as_view())
]
