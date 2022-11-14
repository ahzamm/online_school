from classes.models import Course
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class ListAllCourseSerializer(serializers.ModelSerializer):
    course_detail = serializers.HyperlinkedIdentityField(
        view_name="course:CourseDetail",
        lookup_field="slug",
    )

    class Meta:
        model = Course
        fields = ["name", "course_detail"]


class ListOneCourseSerializer(serializers.ModelSerializer):
    pre_req_courses = ListAllCourseSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = ["name", "course_code", "ch", "pre_req_courses"]
