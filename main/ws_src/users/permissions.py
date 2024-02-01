from rest_framework import permissions

from ws_src.common.choices import BaseUserTypes


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.current_user
        return user.role == BaseUserTypes.DEFAULT_USER
