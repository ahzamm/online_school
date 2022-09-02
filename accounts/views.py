
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (AdminChangePasswordSerializer, AdminChangeTeacherStudentPasswordSerializer,
                                  AdminLoginSerializer, AdminProfileSerializer,
                                  AdminRegisterationSerializer,
                                  StudentChangePasswordSerializer,
                                  StudentLoginSerializer,
                                  StudentProfileSerializer,
                                  StudentRegisterationSerializer,
                                  TeacherChangePasswordSerializer,
                                  TeacherLoginSerializer,
                                  TeacherProfileSerializer,
                                  TeacherRegisterationSerializer)

from .custom_permissions import IsAdmin, IsStudent, IsTeacher


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# ======================= Registeration view =======================


class AdminRegisterationView(APIView):
    def post(self, request):
        serializer = AdminRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': 'Registeration Success', 'token': token},
                        status=201)


class TeacherRegisterationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': 'Registeration Success', 'token': token},
                        status=201)


class StudentRegisterationView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = StudentRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': 'Registeration Success', 'token': token},
                        status=201)

# ======================= Login view =======================


class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'Login Success', 'token': token}, status=200)
        return Response({'error': {'non_field_error': ['Email or Password is not Valid']}},
                        status=400)


class TeacherLoginView(APIView):
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'Login Success', 'token': token}, status=200)
        return Response({'error': {'non_field_error': ['Email or Password is not Valid']}},
                        status=400)


class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'msg': 'Login Success', 'token': token}, status=200)
        return Response({'error': {'non_field_error': ['Email or Password is not Valid']}},
                        status=400)


# ======================= Profile view =======================


class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AdminProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TeacherProfileSerializer(request.user)
        return Response(serializer.data, status=200)


class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = StudentProfileSerializer(request.user)
        return Response(serializer.data, status=200)


# ======================= Change Password view =======================

class AdminChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = AdminChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)
        return Response({'msg': 'password changed successfully'}, status=200)


class TeacherChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = TeacherChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)
        return Response({'msg': 'password changed successfully'}, status=200)


class StudentChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        seriaizer = StudentChangePasswordSerializer(
            data=request.data, context={'user': request.user})
        seriaizer.is_valid(raise_exception=True)
        return Response({'msg': 'password changed successfully'}, status=200)


class AdminChangeTeacherStudentPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminChangeTeacherStudentPasswordSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'password changed successfully'}, status=200)
