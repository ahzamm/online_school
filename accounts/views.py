

from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (AdminLoginSerializer, AdminProfileSerializer,
                                  AdminRegisterationSerializer,
                                  StudentLoginSerializer,
                                  StudentProfileSerializer,
                                  StudentRegisterationSerializer,
                                  TeacherLoginSerializer,
                                  TeacherProfileSerializer,
                                  TeacherRegisterationSerializer)


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
    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'msg': 'Registeration Success', 'token': token},
                        status=201)


class StudentRegisterationView(APIView):
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
