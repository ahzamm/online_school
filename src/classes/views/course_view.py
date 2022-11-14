from accounts.custom_permissions import IsAdmin
from classes.models import Course
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from swagger_responses.classes_responses.classes_responses import (
    course_register_response,
    list_all_course_response,
    list_one_course_response,
)
from utils import ListAllCoursesPagination

from ..messages import (
    COURSE_REGISTER_SUCCESS_MESSAGE,
    COURSE_REGISTER_SUCCESS_STATUS,
)
from ..serializer import (
    CourseSerializer,
    ListAllCourseSerializer,
    ListOneCourseSerializer,
)


class AdminCreateCourseView(GenericAPIView):
    """### For Admin to add new Course"""

    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = CourseSerializer

    @swagger_auto_schema(responses=course_register_response)
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"msg": COURSE_REGISTER_SUCCESS_MESSAGE},
            status=COURSE_REGISTER_SUCCESS_STATUS,
        )


@swagger_auto_schema(responses=list_all_course_response)
class ListAllCoursesView(ListAPIView):
    """### To see all available courses Course"""

    queryset = Course.objects.all()
    serializer_class = ListAllCourseSerializer
    pagination_class = ListAllCoursesPagination


@swagger_auto_schema(responses=list_one_course_response)
class ListOneCourseView(ListAPIView):
    """### To see course detail"""

    serializer_class = ListOneCourseSerializer
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        if queryset := Course.objects.filter(slug=slug):
            return queryset
        else:
            raise NotFound()
