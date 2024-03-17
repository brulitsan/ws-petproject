from django.urls import path

from .views import AutomaticOperationsViewSet, BuyItemViewSet, GetCurrencyInfo

urlpatterns = [
    path("buy_coins/", BuyItemViewSet.as_view({"post": "create"})),
    path("get_coins_info/", GetCurrencyInfo.as_view()),
    path("auto_buy_coins/", AutomaticOperationsViewSet.as_view({"post": "create"}))
]
