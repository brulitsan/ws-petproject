from typing import Any

from ws_src.common.choices import BaseUserTypes

from rest_framework import permissions, request
from rest_framework.viewsets import ViewSet


class IsUser(permissions.BasePermission):
    def has_permission(self, request: request.Request, view: ViewSet) -> Any:
        user = request.current_user
        return user.role == BaseUserTypes.DEFAULT_USER


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: request.Request, view: ViewSet) -> Any:
        user = request.current_user
        return user.role == BaseUserTypes.ADMIN
