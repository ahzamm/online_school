from rest_framework.permissions import BasePermission


class RegisterationPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'ADMIN':
            return True
        return False
