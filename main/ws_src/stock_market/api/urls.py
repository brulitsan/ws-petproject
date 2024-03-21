from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import AutomaticOperationsViewSet, BuyItemViewSet, GetCurrencyInfo

router = SimpleRouter()
router.register('buy_coins', BuyItemViewSet)
router.register('auto_buy_coins', AutomaticOperationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("get_coins_info/", GetCurrencyInfo.as_view()),
]
