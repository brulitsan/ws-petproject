from django.urls import path

from .views import UserView

urlpatterns = [
    path("get_coins_info/", UserView.as_view()),
]
