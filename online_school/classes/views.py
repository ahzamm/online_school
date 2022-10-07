from accounts.custom_permissions import IsAdmin, IsStudent, IsTeacher
from accounts.models import Student
from accounts.models.student_models import StudentMore
from accounts.serializers import ListAllStudentSerializer
from rest_framework import serializers
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import ListAllCoursesPagination

from classes.models import Classes, Course

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
    ListOneCourseSerializer,
    TimeTableSerializer,
)


# DONE
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


# DONE
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


# DONE
class AdminCreateTimeTableView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = TimeTableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"msg": TIMETABLE_REGISTER_SUCCESS_MESSAGE},
            status=TIMETABLE_REGISTER_SUCCESS_STATUS,
        )


# DONE
class ListAllCoursesView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ListAllCourseSerializer
    pagination_class = ListAllCoursesPagination


# Done
class ListOneCourseView(ListAPIView):
    serializer_class = ListOneCourseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return Course.objects.filter(slug=slug)


# Done
class ListAllClassesView(ListAPIView):
    queryset = Classes.objects.all()
    serializer_class = ListAllClassesSerializer
    pagination_class = ListAllCoursesPagination


# This serializer is here because of the problem of circular imports
class ListOneClasseSerializer(serializers.ModelSerializer):

    course = ListAllCourseSerializer(read_only=True)
    teacher_name = serializers.CharField(source="teacher.name")
    student = serializers.SerializerMethodField()

    class Meta:
        model = Classes
        fields = [
            "course",
            "teacher_name",
            "enrollment_start_date",
            "enrollment_end_date",
            "section",
            "mid_exammination_date",
            "final_exammination_date",
            "student",
        ]

    def get_student(self, obj):
        student_query = StudentMore.objects.all().filter(
            user__id__in=obj.student.all(),
        )
        serializer = ListAllStudentSerializer(
            student_query,
            many=True,
            context={"request": self.context.get("request")},
        )

        return serializer.data


# Done
class ListOneClassView(ListAPIView):
    serializer_class = ListOneClasseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        return Classes.objects.filter(slug=slug)

    def get_serializer_context(self):
        context = super(ListOneClassView, self).get_serializer_context()
        context.update({"classes": self.get_queryset()})
        return context


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
        cleared_courses = StudentMore.objects.get(
            user=student,
        ).cleared_course.all()
        for course in pre_req_course:

            if course not in cleared_courses:
                return Response({"data": NOT_ELIGIBLE_MESSAGE}, status=200)

        _class = Classes.objects.get(slug=slug)
        _class.student.add(student)
        _class.save()
        return Response({"data": ENROLLED_SUCCESS_MESSAGE}, status=200)


# create all tests
# yesss
