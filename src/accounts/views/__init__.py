from accounts.views.admin_views import (
    AdminChangePasswordView,
    AdminChangeTeacherStudentPasswordView,
    AdminDeleteClass,
    AdminDeleteCourse,
    AdminDeleteStudent,
    AdminDeleteTeacher,
    AdminLoginView,
    AdminProfileView,
    AdminRegisterationView,
)
from accounts.views.common_views import (
    SendPasswordResetEmailView,
    UserPasswordResetView,
)
from accounts.views.student_views import (
    ListAllStudentView,
    ListOneStudentView,
    StudentChangePasswordView,
    StudentLoginView,
    StudentRegisterationView,
    StudentTimeTableView,
)
from accounts.views.teacher_views import (
    ListAllTeacherView,
    ListOneTeacherView,
    TeacherChangePasswordView,
    TeacherLoginView,
    TeacherRegisterationView,
)
