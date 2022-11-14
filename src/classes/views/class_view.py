from accounts.custom_permissions import (
    IsAdminTeacherStudent,
    IsStudent,
    IsTeacher,
)
from accounts.models import Student
from accounts.models.student_models import StudentMore
from accounts.serializers import ListAllStudentSerializer
from classes.models import Classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from swagger_responses.classes_responses.classes_responses import (
    class_enrollment,
    class_register_response,
    list_all_class_response,
    list_one_class_response,
)
from utils import ListAllCoursesPagination

from ..messages import (
    ALREADY_ENROLLED_MESSAGE,
    CLASS_CREATE_SUCCESS_MESSAGE,
    CLASS_CREATE_SUCCESS_STATUS,
    ENROLLED_SUCCESS_MESSAGE,
    NOT_ELIGIBLE_MESSAGE,
)
from ..serializer import (
    ClassSerializer,
    ListAllClassesSerializer,
    ListAllCourseSerializer,
)


class TeacherCreateClassView(GenericAPIView):
    """### For Teacher to add new Class"""

    permission_classes = [IsAuthenticated, IsTeacher]
    serializer_class = ClassSerializer

    @swagger_auto_schema(responses=class_register_response)
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


@swagger_auto_schema(responses=list_all_class_response)
class ListAllClassesView(ListAPIView):
    """### To see all available classes"""

    queryset = Classes.objects.all()
    serializer_class = ListAllClassesSerializer
    pagination_class = ListAllCoursesPagination
    permission_classes = [IsAuthenticated, IsAdminTeacherStudent]


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


@swagger_auto_schema(responses=list_one_class_response)
class ListOneClassView(ListAPIView):
    """### To see Class details"""

    permission_classes = [IsAuthenticated, IsAdminTeacherStudent]
    serializer_class = ListOneClasseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if queryset := Classes.objects.filter(slug=slug):
            return queryset
        else:
            raise NotFound()

    def get_serializer_context(self):
        context = super(ListOneClassView, self).get_serializer_context()
        context.update({"classes": self.get_queryset()})
        return context


class StudentEnrollClassView(APIView):
    """### For Student to enroll in a class"""

    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = ...

    @swagger_auto_schema(responses=class_enrollment)
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
