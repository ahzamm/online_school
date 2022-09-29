from accounts.custom_permissions import IsAdmin, IsStudent, IsTeacher
from accounts.models import Student
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from classes.models import Classes, Course
from helper import ListAllCoursesPagination

from .messages import (
    ALREADY_ENROLLED_MESSAGE,
    CLASS_CREATE_SUCCESS_MESSAGE,
    CLASS_CREATE_SUCCESS_STATUS,
    COURSE_REGISTER_SUCCESS_MESSAGE,
    COURSE_REGISTER_SUCCESS_STATUS,
    ENROLLED_SUCCESS_MESSAGE,
    NOT_ELIGIBLE_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_STATUS,
)
from .serializer import (
    ClassSerializer,
    CourseSerializer,
    ListAllClassesSerializer,
    ListAllCourseSerializer,
    ListOneClasseSerializer,
    ListOneCourseSerializer,
    TimeTableSerializer,
)


class AdminCreateCourseView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": COURSE_REGISTER_SUCCESS_MESSAGE},
            status=COURSE_REGISTER_SUCCESS_STATUS,
        )


class TeacherCreateClassView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request):
        teacher = request.user
        serializer = ClassSerializer(
            data=request.data,
            context={"teacher": teacher},
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": CLASS_CREATE_SUCCESS_MESSAGE},
            status=CLASS_CREATE_SUCCESS_STATUS,
        )


class AdminCreateTimeTableView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": TIMETABLE_REGISTER_SUCCESS_MESSAGE},
            status=TIMETABLE_REGISTER_SUCCESS_STATUS,
        )


# TODO
# courses should have other pre req courses
# Student can see all availabel classes
# student can enroll themself in a class of a course they are eligable of(they
# have already cleared pre req classes of that course)
# Teacher can create and insert Attendence


class ListAllCoursesView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ListAllCourseSerializer
    pagination_class = ListAllCoursesPagination


class ListOneCourseView(ListAPIView):
    serializer_class = ListOneCourseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return Course.objects.filter(slug=slug)


# student can see all classes


class ListAllClassesView(ListAPIView):
    queryset = Classes.objects.all()
    serializer_class = ListAllClassesSerializer
    pagination_class = ListAllCoursesPagination


class ListOneClassView(ListAPIView):
    serializer_class = ListOneClasseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return Classes.objects.filter(slug=slug)


# [ x ] student can not enrolled in two class of same course DONE
# [   ] Now course pre req logic
# as soon as a student is created, StudentMore for that Student should bhe
# created


class StudentEnrollClassView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, slug):
        request.user.__class__ = Student
        student = request.user
        if Classes.objects.filter(slug=slug, student=student):
            return Response(
                {"data": ALREADY_ENROLLED_MESSAGE},
                status=200,
            )

        course = Classes.objects.get(slug=slug).course
        pre_req_course = course.pre_req_courses.all()
        for course in pre_req_course:
            if course not in student.more.cleared_course.all():
                return Response({"data": NOT_ELIGIBLE_MESSAGE}, status=200)

        _class = Classes.objects.get(slug=slug)
        _class.student.add(student)
        _class.save()
        return Response({"data": ENROLLED_SUCCESS_MESSAGE}, status=200)
