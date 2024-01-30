from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import SimpleRouter

from .views import StockMarketView, BuyItemViewSet

buy_items_router = SimpleRouter()
buy_items_router.register(r'buy_items', BuyItemViewSet, basename='buy_items')


urlpatterns = [
    path('get_coins/', StockMarketView.as_view()),
    path('buy_coins/', BuyItemViewSet.as_view({'post': 'create'})),
    # path('sale_coins/', SellItemsView.as_view()),
]
