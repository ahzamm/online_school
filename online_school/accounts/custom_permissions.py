from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "ADMIN"


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "TEACHER"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "STUDENT"


class IsTeacherStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.type in ["TEACHER", "STUDENT"]


class IsAdminTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.type in ["ADMIN", "TEACHER"]


class IsAdminStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.type in ["ADMIN", "STUDENT"]


class IsAdminTeacherStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.type in ["ADMIN", "TEACHER", "STUDENT"]
