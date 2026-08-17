from rest_framework.permissions import BasePermission


class IsPremiumUser(BasePermission):
    """
    Custom permission to allow access only to premium users (is_premium=True).
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_premium", False)
        )
