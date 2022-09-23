

from accounts.custom_permissions import IsAdmin
from accounts.generate_tokens import get_tokens_for_user
from accounts.messages import (ADMIN_REGISTERATION_SUCCESS_MESSAGE,
                               EMAIL_PASSWORD_NOT_VALID_MESSAGE,
                               EMAIL_PASSWORD_NOT_VALID_STATUS,
                               LOGIN_SUCCESS_MESSAGE, LOGIN_SUCCESS_STATUS,
                               PASSWORD_CHANGE_SUCCESS_MESSAGE,
                               PASSWORD_CHANGE_SUCCESS_STATUS,
                               REGISTERATION_SUCCESS_STATUS)
from accounts.serializers import (AdminChangePasswordSerializer,
                                  AdminChangeTeacherStudentPasswordSerializer,
                                  AdminLoginSerializer, AdminProfileSerializer,
                                  AdminRegisterationSerializer)
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AdminRegisterationView(APIView):
    def post(self, request):
        serializer = AdminRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)

        return Response({'msg': ADMIN_REGISTERATION_SUCCESS_MESSAGE,
                        'token': token},
                        status=REGISTERATION_SUCCESS_STATUS)


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'errors': {'non_field_errors':
                                        [EMAIL_PASSWORD_NOT_VALID_MESSAGE]}},
                            status=EMAIL_PASSWORD_NOT_VALID_STATUS)

        return Response({'msg': LOGIN_SUCCESS_MESSAGE,
                        'token': get_tokens_for_user(user)},
                        status=LOGIN_SUCCESS_STATUS)


class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        serializer = AdminProfileSerializer(request.user)

        return Response(serializer.data, status=200)


class AdminChangeTeacherStudentPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminChangeTeacherStudentPasswordSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)


class AdminChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = AdminChangePasswordSerializer(data=request.data,
                                                  context={'user':
                                                           request.user})
        seriaizer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)
