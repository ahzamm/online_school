
from django.urls import path

from .views import (AdminLoginView, AdminRegisterationView,
                    StudentRegisterationView, TeacherRegisterationView)

urlpatterns = [
    path('admin-register/', AdminRegisterationView.as_view(),
         name='Admin_Register'),
    path('teacher-register/', TeacherRegisterationView.as_view(),
         name='Teacher_Register'),
    path('student-register/', StudentRegisterationView.as_view(),
         name='Student_Register'),

    path('admin-login/', AdminLoginView.as_view(),
         name='Admin_Login'),
]
