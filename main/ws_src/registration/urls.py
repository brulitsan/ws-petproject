from ws_src.registration.api_handlers import LoginView, RefreshTokenView, RegisterUserView

from django.urls import path

urlpatterns = [
    path("register/", RegisterUserView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh-token/", RefreshTokenView.as_view()),
]
