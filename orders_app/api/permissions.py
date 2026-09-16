from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    """Allow access to authenticated customer users."""

    def has_permission(self, request, view):
        """Check whether the requester has a customer profile."""
        return request.user.is_authenticated and request.user.profile.type == 'customer'


class IsBusiness(BasePermission):
    """Allow access to authenticated business users."""

    def has_permission(self, request, view):
        """Check whether the requester has a business profile."""
        return request.user.is_authenticated and request.user.profile.type == 'business'
