from users.models import UserRoleChoices
from rest_framework import permissions


class IsBuyerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated \
               and (request.user.is_staff or request.user.role == UserRoleChoices.BUYER)
