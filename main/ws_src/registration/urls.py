from django.urls import path

from registration.api_handlers import RegisterUserView, AssignTokenView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('assign-token/', AssignTokenView.as_view(), name='assign-token'),
]