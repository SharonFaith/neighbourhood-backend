from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser