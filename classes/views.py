
import json

from accounts.custom_permissions import IsAdmin, IsTeacher
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classes.models import Course

from .helper import UUIDEncoder
from .messages import (CLASS_CREATE_SUCCESS_MESSAGE,
                       CLASS_CREATE_SUCCESS_STATUS,
                       COURSE_REGISTER_SUCCESS_MESSAGE,
                       COURSE_REGISTER_SUCCESS_STATUS,
                       TIMETABLE_REGISTER_SUCCESS_MESSAGE,
                       TIMETABLE_REGISTER_SUCCESS_STATUS)
from .serializer import ClassSerializer, CourseSerializer, ListAllCourseSerializer, TimeTableSerializer


class AdminCreateCourse(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'msg': COURSE_REGISTER_SUCCESS_MESSAGE},
                        status=COURSE_REGISTER_SUCCESS_STATUS)


class TeacherCreateClassView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = request.user
        serializer = ClassSerializer(data=request.data, context={
                                     'teacher': teacher})
        serializer.is_valid(raise_exception=True)

        return Response({'msg': CLASS_CREATE_SUCCESS_MESSAGE},
                        status=CLASS_CREATE_SUCCESS_STATUS)


class AdminCreateTimeTable(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'msg': TIMETABLE_REGISTER_SUCCESS_MESSAGE},
                        status=TIMETABLE_REGISTER_SUCCESS_STATUS)


# TODO
# courses should have other pre req courses
# Student can see all availabel classes
# student can enroll themself in a class of a course they are eligable of(they
# have already cleared pre req classes of that course)
# Teacher can create and insert Attendence


# TODO
# list all courses
# list all classes

class ListAllCoursesView(APIView):
    def get(self, request):
        data = Course.objects.all().values('name')
        serializer = ListAllCourseSerializer(data, many=True)
        json_data = json.dumps(serializer.data, cls=UUIDEncoder)
        json_without_slash = json.loads(json_data)

        return Response({'data': json_without_slash}, status=200)
from django.core import serializers
from django.forms.models import model_to_dict

class ListOneCourse(APIView):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        serializer = model_to_dict(course)

        for iter, i in enumerate(serializer['pre_req_courses']):
            serializer['pre_req_courses'][iter] = i.name
            
        json_data = json.dumps(serializer, cls=UUIDEncoder)
        json_without_slash = json.loads(json_data)
        del json_without_slash['slug']

        return Response({'data': json_without_slash}, status=200)
