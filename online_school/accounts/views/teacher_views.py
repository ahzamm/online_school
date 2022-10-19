from accounts.custom_permissions import IsAdmin
from accounts.generate_tokens import get_tokens_for_user
from accounts.messages import (
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CHANGE_SUCCESS_MESSAGE,
    PASSWORD_CHANGE_SUCCESS_STATUS,
    REGISTERATION_SUCCESS_STATUS,
    TEACHER_REGISTERATION_SUCCESS_MESSAGE,
)
from accounts.models import TeacherMore
from accounts.serializers import (
    TeacherChangePasswordSerializer,
    TeacherLoginSerializer,
    TeacherRegisterationSerializer,
)
from accounts.serializers.teacher_serializers import ListOneTeacherSerializer
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.accounts_responses.teacher_responses import (
    teacher_change_password_response,
    teacher_login_response,
    teacher_register_response,
)
from utils.flatten_dict import flatten_dict


class TeacherRegisterationView(GenericAPIView):
    """## For Teacher **`Registeration`**"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = TeacherRegisterationSerializer

    @swagger_auto_schema(responses=teacher_register_response)
    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        try:
            TeacherMore.objects.create(
                user=user,
                tea_id=request.data.get("tea_id"),
            )
        except Exception:
            from rest_framework import serializers

            raise serializers.ValidationError(
                "User with This Teacher ID Already Present"
            )

        return Response(
            {"msg": TEACHER_REGISTERATION_SUCCESS_MESSAGE, "token": token},
            status=REGISTERATION_SUCCESS_STATUS,
        )


class TeacherLoginView(GenericAPIView):
    """## For Teacher **`Login`**"""

    serializer_class = TeacherLoginSerializer

    @swagger_auto_schema(responses=teacher_login_response)
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            return Response(
                {
                    "errors": {
                        "non_field_errors": [
                            EMAIL_PASSWORD_NOT_VALID_MESSAGE,
                        ],
                    },
                },
                status=EMAIL_PASSWORD_NOT_VALID_STATUS,
            )

        return Response(
            {"msg": LOGIN_SUCCESS_MESSAGE, "token": get_tokens_for_user(user)},
            status=LOGIN_SUCCESS_STATUS,
        )


class TeacherChangePasswordView(GenericAPIView):
    """## For Teacher to his/her account's **`password`**"""

    permission_classes = [IsAuthenticated]
    serializer_class = TeacherChangePasswordSerializer

    @swagger_auto_schema(responses=teacher_change_password_response)
    def post(self, request):
        seriaizer = TeacherChangePasswordSerializer(
            data=request.data,
            context={"user": request.user},
        )
        seriaizer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_CHANGE_SUCCESS_MESSAGE},
            status=PASSWORD_CHANGE_SUCCESS_STATUS,
        )


# @swagger_auto_schema(responses=List_one_student_response)
class ListOneTeacherView(ListAPIView):
    """## For See details of a **`Student`**"""

    serializer_class = ListOneTeacherSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return TeacherMore.objects.filter(slug=slug)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            response.data = flatten_dict(response.data[0])
            return response
        except Exception:
            return response
