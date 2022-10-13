from accounts.custom_permissions import IsAdmin, IsStudent
from accounts.generate_tokens import get_tokens_for_user
from accounts.messages import (
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CHANGE_SUCCESS_MESSAGE,
    PASSWORD_CHANGE_SUCCESS_STATUS,
    REGISTERATION_SUCCESS_STATUS,
    STUDENT_REGISTERATION_SUCCESS_MESSAGE,
)
from accounts.models.student_models import StudentMore
from accounts.serializers import (
    ListAllStudentSerializer,
    ListOneStudentSerializer,
    StudentChangePasswordSerializer,
    StudentLoginSerializer,
    StudentProfileSerializer,
    StudentRegisterationSerializer,
)
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.accounts_responses.student_responses import (
    List_all_student_response,
    List_one_student_response,
    student_change_ts_password_response,
    student_login_response,
    student_profile_response,
    student_register_response,
)
from utils.custom_paginations import ListAllStudentPagination
from utils.flatten_dict import flatten_dict


class StudentRegisterationView(GenericAPIView):
    """## For Student **`Registeration`**"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = StudentRegisterationSerializer

    @swagger_auto_schema(responses=student_register_response)
    def post(self, request):
        serializer = StudentRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        StudentMore.objects.create(
            user=user,
            roll_no=request.data.get("roll_no"),
        )

        return Response(
            {"msg": STUDENT_REGISTERATION_SUCCESS_MESSAGE, "token": token},
            status=REGISTERATION_SUCCESS_STATUS,
        )


class StudentLoginView(GenericAPIView):
    """## For Student **`Login`**"""

    serializer_class = StudentLoginSerializer

    @swagger_auto_schema(responses=student_login_response)
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
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


class StudentProfileView(GenericAPIView):
    """## For Student to view his/her **`Profile`**"""

    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StudentProfileSerializer

    @swagger_auto_schema(responses=student_profile_response)
    def get(self, request):
        serializer = StudentProfileSerializer(request.user)

        return Response(serializer.data, status=200)


class StudentChangePasswordView(GenericAPIView):
    """## For Student to change his/her account's **`password`**"""

    permission_classes = [IsAuthenticated]
    serializer_class = StudentChangePasswordSerializer

    @swagger_auto_schema(responses=student_change_ts_password_response)
    def post(self, request):
        seriaizer = StudentChangePasswordSerializer(
            data=request.data,
            context={"user": request.user},
        )
        seriaizer.is_valid(raise_exception=True)

        return Response(
            {"msg": PASSWORD_CHANGE_SUCCESS_MESSAGE},
            status=PASSWORD_CHANGE_SUCCESS_STATUS,
        )


class ListOneStudentView(ListAPIView):
    """## For See details of a **`Student`**"""

    serializer_class = ListOneStudentSerializer
    lookup_url_kwarg = "slug"

    @swagger_auto_schema(responses=List_one_student_response)
    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return StudentMore.objects.filter(slug=slug)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = flatten_dict(response.data[0])
        return response


@swagger_auto_schema(responses=List_all_student_response)
class ListAllStudentView(ListAPIView):
    """### To see all **`Students`**"""

    queryset = StudentMore.objects.all()
    serializer_class = ListAllStudentSerializer
    pagination_class = ListAllStudentPagination
