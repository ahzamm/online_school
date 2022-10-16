from accounts.views.admin_views import (
    AdminChangePasswordView,
    AdminChangeTeacherStudentPasswordView,
    AdminLoginView,
    AdminProfileView,
    AdminRegisterationView,
)
from accounts.views.common_views import (
    SendPasswordResetEmailView,
    UserPasswordResetView,
)
from accounts.views.student_views import (
    StudentChangePasswordView,
    StudentLoginView,
    StudentRegisterationView,
    ListAllStudentView,
)
from accounts.views.teacher_views import (
    TeacherChangePasswordView,
    TeacherLoginView,
    TeacherProfileView,
    TeacherRegisterationView,
)
