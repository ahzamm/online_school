from accounts.custom_permissions import IsAdmin, IsTeacher
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
from accounts.serializers import (
    TeacherChangePasswordSerializer,
    TeacherLoginSerializer,
    TeacherProfileSerializer,
    TeacherRegisterationSerializer,
)
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TeacherRegisterationView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = TeacherRegisterationSerializer

    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        # we will create StudentMore object for a student at the time of
        # student creation to use latter

        return Response(
            {"msg": TEACHER_REGISTERATION_SUCCESS_MESSAGE, "token": token},
            status=REGISTERATION_SUCCESS_STATUS,
        )


class TeacherLoginView(GenericAPIView):
    serializer_class = TeacherLoginSerializer

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


class TeacherProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = TeacherProfileSerializer

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)

        return Response(serializer.data, status=200)


class TeacherChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherChangePasswordSerializer

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