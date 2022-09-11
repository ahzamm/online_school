from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'ADMIN':
            return True
        return False


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'TEACHER':
            return True
        return False


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'STUDENT':
            return True
        return False
