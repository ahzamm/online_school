from classes.models import Classes, Course
from rest_framework import serializers

from ..messages import CLASS_ALREADY_REGISTERED, NO_COURSE_ERROR_MESSAGE


class ClassSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(max_length=10)

    class Meta:
        model = Classes
        exclude = ["student", "course"]

    def validate(self, data):
        enrollment_start_date = data.get("enrollment_start_date")
        enrollment_end_date = data.get("enrollment_end_date")
        course_code = data.get("course_code")
        section = data.get("section")

        if not Course.objects.filter(course_code=course_code).exists():
            raise serializers.ValidationError(NO_COURSE_ERROR_MESSAGE)

        course_id = Course.objects.get(course_code=course_code).id

        if Classes.objects.filter(
            course_id=course_id,
            section=section,
        ).exists():

            raise serializers.ValidationError(CLASS_ALREADY_REGISTERED)

        teacher = self.context.get("teacher")
        classes: Classes = Classes.objects.create(
            enrollment_start_date=enrollment_start_date,
            enrollment_end_date=enrollment_end_date,
            teacher=teacher,
            section=section,
            course=Course.objects.get(course_code=course_code),
        )

        classes.save()

        return data


class ListAllClassesSerializer(serializers.ModelSerializer):
    class_detail = serializers.HyperlinkedIdentityField(
        view_name="course:ClassDetail",
        lookup_field="slug",
    )
    course_name = serializers.CharField(source="course.name")

    class Meta:
        model = Classes
        fields = ["course_name", "section", "class_detail"]
