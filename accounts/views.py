

from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import (AdminRegisterationSerializer,
                                  StudentRegisterationSerializer,
                                  TeacherRegisterationSerializer)


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


class UserLoginView(APIView):
    def post(self, request):
        return Response({'msg': 'Login Success'}, status=200)
