from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Hood

User = get_user_model()

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


class IsHoodUser(BasePermission):
    def has_permission(self, request, view):
        hood_id = request.GET.get('hood_id')
        user_id = request.GET.get('user_id')
        user =User.objects.filter(id = user_id).first()
        hood =Hood.objects.filter(id = hood_id).first()
        if hood_id is not None and user_id is not None:
            if user.hood == hood.name:
                return True
        else:
            return request.user.is_superuser


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff

#if user id in request returh that particular hood that corresponds to their hoodo