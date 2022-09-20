from rest_framework import serializers
from .models import Classes, Course, TimeTable
from .messages import *


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        pre_req_course = data.get('pre_req_course')

        if pre_req_course is None:
            data['pre_req_level'] = 1


class TimeTableSerializer(serializers.ModelSerializer):
    _class_ = serializers.UUIDField()

    class Meta:
        model = TimeTable
        exclude = ['_class']

    def validate(self, data):
        days = data.get('days')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        room_no = data.get('room_no')
        _class = data.get('_class_')
        is_class_exists = Classes.objects.filter(id=_class).exists()

        if not is_class_exists:
            raise serializers.ValidationError(no_class_found(_class))

        if start_time > end_time:
            raise serializers.ValidationError(INVALID_TIME_MESSAGE)

        if TimeTable.objects.filter(start_time__lt=end_time,
                                    end_time__gt=start_time,
                                    room_no=room_no,
                                    days=days).exists():

            raise serializers.ValidationError(
                timetable_clash_message(room_no))

        timetable: TimeTable = TimeTable.objects.create(
            days=days,
            start_time=start_time,
            end_time=end_time,
            room_no=room_no,
            _class=Classes.objects.get(id=_class),
        )

        timetable.save()

        return data


class ClassSerializer(serializers.ModelSerializer):
    course_code = serializers.CharField(max_length=10)

    class Meta:
        model = Classes
        exclude = ['student', 'course']

    def validate(self, data):
        enrollment_start_date = data.get('enrollment_start_date')
        enrollment_end_date = data.get('enrollment_end_date')
        course_code = data.get('course_code')
        section = data.get('section')

        if not Course.objects.filter(course_code=course_code).exists():

            raise serializers.ValidationError(NO_COURSE_ERROR_MESSAGE)

        course_id = Course.objects.get(course_code=course_code).id

        if Classes.objects.filter(course_id=course_id,
                                  section=section).exists():

            raise serializers.ValidationError(CLASS_ALREADY_REGISTERED)

        teacher = self.context.get('teacher')
        classes: Classes = Classes.objects.create(
            enrollment_start_date=enrollment_start_date,
            enrollment_end_date=enrollment_end_date,
            teacher=teacher,
            section=section,
            course=Course.objects.get(course_code=course_code),
        )

        classes.save()

        return data
