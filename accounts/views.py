
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import *

from .custom_permissions import IsAdmin, IsStudent, IsTeacher
from .messages import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class AdminRegisterationView(APIView):
    def post(self, request):
        serializer = AdminRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response({'msg': ADMIN_REGISTERATION_SUCCESS_MESSAGE,
                        'token': token},
                        status=REGISTERATION_SUCCESS_STATUS)


class TeacherRegisterationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response({'msg': TEACHER_REGISTERATION_SUCCESS_MESSAGE,
                        'token': token},
                        status=REGISTERATION_SUCCESS_STATUS)


class StudentRegisterationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = StudentRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response({'msg': STUDENT_REGISTERATION_SUCCESS_MESSAGE,
                        'token': token},
                        status=REGISTERATION_SUCCESS_STATUS)


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': LOGIN_SUCCESS_MESSAGE, 'token': token},
                            status=LOGIN_SUCCESS_STATUS)

        return Response({'errors': {'non_field_errors': [EMAIL_PASSWORD_NOT_VALID_MESSAGE]}},
                        status=EMAIL_PASSWORD_NOT_VALID_STATUS)


class TeacherLoginView(APIView):
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': LOGIN_SUCCESS_MESSAGE,
                            'token': token},
                            status=LOGIN_SUCCESS_STATUS)

        return Response({'errors': {'non_field_errors': [EMAIL_PASSWORD_NOT_VALID_MESSAGE]}},
                        status=EMAIL_PASSWORD_NOT_VALID_STATUS)


class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': LOGIN_SUCCESS_MESSAGE,
                            'token': token},
                            status=LOGIN_SUCCESS_STATUS)

        return Response({'errors': {'non_field_errors': [EMAIL_PASSWORD_NOT_VALID_MESSAGE]}},
                        status=EMAIL_PASSWORD_NOT_VALID_STATUS)


class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        serializer = AdminProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        serializer = StudentProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class AdminChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = AdminChangePasswordSerializer(data=request.data,
                                                  context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)


class TeacherChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = TeacherChangePasswordSerializer(data=request.data,
                                                    context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)


class StudentChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = StudentChangePasswordSerializer(data=request.data,
                                                    context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)


class AdminChangeTeacherStudentPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminChangeTeacherStudentPasswordSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)


class SendPasswordResetEmailView(APIView):
    def post(self, request):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({"msg": PASSWORD_RESET_EMAIL_MESSAGE},
                        status=PASSWORD_RESET_EMAIL_STATUS)


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data,
                                                 context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_RESET_SUCCESS_MESSAGE},
                        status=PASSWORD_RESET_SUCCESS_STATUS)
