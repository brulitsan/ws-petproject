from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

from ws_src.registration.dependencies import is_authenticated


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = is_authenticated(request)
        request.current_user = user
        if request.current_user == AnonymousUser:
            request.current_user = False
        response = self.get_response(request)
        return response
