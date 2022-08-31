
from django.urls import path

from .views import (AdminLoginView, AdminProfileView, AdminRegisterationView,
                    StudentLoginView, StudentRegisterationView,
                    TeacherLoginView, TeacherRegisterationView)

urlpatterns = [
    path('admin-register/', AdminRegisterationView.as_view(),
         name='Admin_Register'),
    path('teacher-register/', TeacherRegisterationView.as_view(),
         name='Teacher_Register'),
    path('student-register/', StudentRegisterationView.as_view(),
         name='Student_Register'),

    path('admin-login/', AdminLoginView.as_view(),
         name='Admin_Login'),
    path('teacher-login/', TeacherLoginView.as_view(),
         name='Teacher_Login'),
    path('student-login/', StudentLoginView.as_view(),
         name='Student_Login'),

    path('admin-profile/', AdminProfileView.as_view(),
         name='Admin_Login'),
    path('teacher-profile/', AdminProfileView.as_view(),
         name='Teacher_Login'),
    path('student-profile/', AdminProfileView.as_view(),
         name='Student_Login'),
]
