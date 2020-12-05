from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny, IsAuthenticated

    

class IsActivatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_active

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_active

class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

#if user id in request returh that particular hood that corresponds to their hoodo