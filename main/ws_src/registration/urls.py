from django.urls import path

from registration.api_handlers import RegisterUserView, RefreshTokenView, LoginView

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
]
