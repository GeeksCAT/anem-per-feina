from typing import Any, Sequence

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from django.utils.translation import ugettext as _
from django.views import View

JOB_AUTHOR_METHODS: Sequence[str] = ("PUT", "PATCH", "DELETE")


class IsAuthorOrReadOnly(BasePermission):
    # TODO: Improve message
    message = _("Unauthorized")

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """
        Object-level permission to only allow user model manipulation
        """
        # Anonymous user methods
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in JOB_AUTHOR_METHODS and (request.user.id == obj.user_id):
            return True
        return False


class IsSelfOrReadOnly(BasePermission):
    # TODO: Improve message
    message = _("Unauthorized")

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """
        Object-level permission to only allow user model manipulation
        """
        return bool(request.method in permissions.SAFE_METHODS or request.user.id == obj.id)
