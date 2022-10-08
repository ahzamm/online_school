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
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.flatten_dict import flatten_dict
from utils.custom_paginations import ListAllStudentPagination


class StudentRegisterationView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = StudentRegisterationSerializer

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
    serializer_class = StudentLoginSerializer

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
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = StudentProfileSerializer

    def get(self, request):
        serializer = StudentProfileSerializer(request.user)

        return Response(serializer.data, status=200)


class StudentChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentChangePasswordSerializer

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
    serializer_class = ListOneStudentSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return StudentMore.objects.filter(slug=slug)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = flatten_dict(response.data[0])
        return response


class ListAllStudentView(ListAPIView):
    queryset = StudentMore.objects.all()
    serializer_class = ListAllStudentSerializer
    pagination_class = ListAllStudentPagination