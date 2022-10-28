from accounts.custom_permissions import (
    IsAdmin,
    IsAdminTeacher,
    IsAdminTeacherStudent,
    IsTeacher,
)
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
    ListAllTeacherSerializer,
    ListOneTeacherSerializer,
    TeacherChangePasswordSerializer,
    TeacherLoginSerializer,
    TeacherRegisterationSerializer,
)
from django.contrib.auth import authenticate
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.accounts_responses.teacher_responses import (
    teacher_change_password_response,
    teacher_login_response,
    teacher_register_response,
    List_one_teacher_response,
    list_all_teacher_response,
)
from utils.custom_paginations import ListAllTeacherPagination
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
            TeacherMore.objects.create(user=user, tea_id=request.data.get("tea_id"))
        except IntegrityError:
            # If the Roll Number validation failed, then saved student must be deleted
            user.delete()
            raise serializers.ValidationError(
                "Teacher With this Teacher ID Number already Exists",
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

    permission_classes = [IsAuthenticated, IsTeacher]
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


@swagger_auto_schema(responses=List_one_teacher_response)
class ListOneTeacherView(ListAPIView):
    """## To See details of a **`Teacher`**"""

    serializer_class = ListOneTeacherSerializer
    lookup_url_kwarg = "slug"
    permission_classes = [IsAuthenticated, IsAdminTeacher]

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        queryset = TeacherMore.objects.filter(slug=slug)
        if queryset:
            return queryset
        else:
            raise NotFound()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            response.data = flatten_dict(response.data[0])
            return response
        except Exception:
            return response


@swagger_auto_schema(responses=list_all_teacher_response)
class ListAllTeacherView(ListAPIView):
    """### To see all **`Teachers`**"""

    queryset = TeacherMore.objects.all()
    serializer_class = ListAllTeacherSerializer
    pagination_class = ListAllTeacherPagination
    permission_classes = [IsAuthenticated, IsAdminTeacherStudent]
