from rest_framework import permissions

class isowner_readonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser==1 or request.user.is_staff==1:return True
        return request.user==obj.owner