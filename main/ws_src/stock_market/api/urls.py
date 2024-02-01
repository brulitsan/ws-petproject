from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import SimpleRouter

from .views import StockMarketViewSet, BuyItemViewSet

urlpatterns = [
    path('get_coins/', StockMarketViewSet.as_view({'get': 'list'})),
    path('buy_coins/', BuyItemViewSet.as_view({'post': 'create'})),
    # path('sale_coins/', SellItemsView.as_view()),
]
