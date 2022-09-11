from rest_framework import serializers
from .models import Course
from accounts.models import Teacher


class CourseSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = Course
        exclude = ['teacher']

    def validate(self, data):

        name = data.get('name')
        course_code: Course.course_code = data.get('course_code')
        ch = data.get('ch')
        email = data.get('email')
        teacher: Teacher = Teacher.objects.filter(email=email)
        if teacher:
            course: Course = Course.objects.create(
                name=name, course_code=course_code, ch=ch, teacher=Teacher.objects.get(email=email))

            course.save()
            return data
        else:
            raise serializers.ValidationError(
                'No teacher with this email found')
