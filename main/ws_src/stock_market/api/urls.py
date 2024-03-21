from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AutomaticOperationsViewSet, BuyItemViewSet, GetCurrencyInfo

router = SimpleRouter()
router.register(r'buy_coins', BuyItemViewSet, basename='buy-item')
router.register(r'auto_buy_coins', AutomaticOperationsViewSet, basename='auto-buy-item')

urlpatterns = [
    path('', include(router.urls)),
    path("get_coins_info/", GetCurrencyInfo.as_view()),
]
