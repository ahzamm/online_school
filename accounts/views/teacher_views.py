
from accounts.custom_permissions import IsAdmin, IsTeacher
from accounts.generate_tokens import get_tokens_for_user
from accounts.messages import *
from accounts.serializers import *
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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

        return Response({'errors': {'non_field_errors':
                                    [EMAIL_PASSWORD_NOT_VALID_MESSAGE]}},
                        status=EMAIL_PASSWORD_NOT_VALID_STATUS)


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class TeacherChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = TeacherChangePasswordSerializer(data=request.data,
                                                    context={'user':
                                                             request.user})
        seriaizer.is_valid(raise_exception=True)

        return Response({'msg': PASSWORD_CHANGE_SUCCESS_MESSAGE},
                        status=PASSWORD_CHANGE_SUCCESS_STATUS)