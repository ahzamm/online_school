from .admin_serializers import (
    AdminChangePasswordSerializer,
    AdminChangeTeacherStudentPasswordSerializer,
    AdminLoginSerializer,
    AdminProfileSerializer,
    AdminRegisterationSerializer,
)
from .common_serializers import (
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
)
from .students_serializers import (
    ListAllStudentSerializer,
    ListOneStudentSerializer,
    StudentChangePasswordSerializer,
    StudentLoginSerializer,
    StudentRegisterationSerializer,
)
from .teacher_serializers import (
    ListAllTeacherSerializer,
    ListOneTeacherSerializer,
    TeacherChangePasswordSerializer,
    TeacherLoginSerializer,
    TeacherProfileSerializer,
    TeacherRegisterationSerializer,
)
