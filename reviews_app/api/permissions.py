from rest_framework.permissions import BasePermission


class IsReviewOwner(BasePermission):
    """Allow changes only to the user who wrote a review."""

    def has_object_permission(self, request, view, obj):
        """Check whether the requester owns the review."""
        return obj.reviewer == request.user
    