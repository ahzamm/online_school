
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'ADMIN'


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'TEACHER'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.type == 'STUDENT'
