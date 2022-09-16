# from django.shortcuts import render

# Create your views here.
# TODO
# - admin can create Course
# - admin can create TimeTable
# - Teacher can create class
# - Teacher can create and insert Attendence


from accounts.custom_permissions import IsAdmin, IsTeacher
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .messages import *
from .serializer import ClassSerializer, CourseSerializer, TimeTableSerializer

# Response = requests.models.Response


class AdminCreateCourse(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': COURSE_REGISTER_SUCCESS_MESSAGE},
                        status=COURSE_REGISTER_SUCCESS_STATUS)


# TODO
# Teacher create class view
# create course fixture complete
# i just have to complete create class fixture

class AdminCreateTimeTable(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': TIMETABLE_REGISTER_SUCCESS_MESSAGE},
                        status=TIMETABLE_REGISTER_SUCCESS_STATUS)


class TeacherCreateClassView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher_email = request.user.email

        serializer = ClassSerializer(data=request.data, context={
                                     'teacher_email': teacher_email})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': CLASS_CREATE_SUCCESS_MESSAGE},
                        status=CLASS_CREATE_SUCCESS_STATUS)
