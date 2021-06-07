from rest_framework.permissions import BasePermission

class IsAdvertisementOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):

        return (request.user.is_authenticated and
                (request.user == obj.creator)) or request.user.is_superuser