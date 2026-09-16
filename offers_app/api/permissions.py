from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsBusinessUser(BasePermission):
    """Allow offer creation only for authenticated business users."""
    message = "Only business users can create offers."

    def has_permission(self, request, view):
        """Check whether the request may access the offer collection."""
        if request.method == 'GET':
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.profile.type == 'business'

class IsCreatorOffers(BasePermission):
    """Allow modifications only to the user who owns an offer."""

    message = "Only the offer creator can change this offer."

    def has_object_permission(self, request, view, obj):
        """Check ownership for unsafe requests while allowing reads."""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user