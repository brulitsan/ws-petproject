from django.urls import path
from ws_src.registration.api_handlers import (LoginView, RefreshTokenView,
                                              RegisterUserView)

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh-token/", RefreshTokenView.as_view()),
]
