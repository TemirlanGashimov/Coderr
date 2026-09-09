from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsBusinessUser(BasePermission):
    message = "Only business users can create offers."

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True

        if not request.user.is_authenticated:
            return False

        return request.user.profile.type == 'business'

class IsCreatorOffers(BasePermission):
    message = "Only Creater this Offers can canchange it."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user