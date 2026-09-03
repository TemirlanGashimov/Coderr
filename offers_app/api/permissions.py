from rest_framework.permissions import BasePermission


class IsBusinessUser(BasePermission):
    message = "Only business users can create offers."

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.profile.type == 'business'