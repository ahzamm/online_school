
from django.urls import path

from .views import *

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
         name='Admin_Profile'),
    path('teacher-profile/', TeacherProfileView.as_view(),
         name='Teacher_Profile'),
    path('student-profile/', StudentProfileView.as_view(),
         name='Student_Profile'),


    path('admin-change-password/', AdminChangePasswordView.as_view(),
         name='Admin_Change_Password'),
    path('teacher-change-password/', TeacherChangePasswordView.as_view(),
         name='Teacher_Change_Password'),
    path('student-change-password/', StudentChangePasswordView.as_view(),
         name='Student_Change_Password'),

    path('admin-change-teastu-password/', AdminChangeTeacherStudentPasswordView.as_view(),
         name='Admin_Change_TeaStu_Password'),

    path('reset-password/', SendPasswordResetEmailView.as_view(),
         name="Admin_Reset_Password"),
    path('reset/<uid>/<token>/',
         UserPasswordResetView.as_view(), name='reset-password'),
]
