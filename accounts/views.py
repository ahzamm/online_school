

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.renderers import UserRender
from accounts.serializers import (AdminLoginSerializer,
                                  AdminRegisterationSerializer,
                                  StudentRegisterationSerializer,
                                  TeacherRegisterationSerializer)


# ======================= Registeration view =======================
class AdminRegisterationView(APIView):
    def post(self, request):
        serializer = AdminRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registeration Success'}, status=201)


class TeacherRegisterationView(APIView):
    def post(self, request):
        serializer = TeacherRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registeration Success'}, status=201)


class StudentRegisterationView(APIView):
    def post(self, request):
        serializer = StudentRegisterationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg': 'Registeration Success'}, status=201)


# ======================= Login view =======================

class AdminLoginView(APIView):
    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            return Response({'msg': 'Login Success'}, status=200)
        return Response({'error': {'non_field_error': ['Email or Password is not Valid']}},
                        status=400)
