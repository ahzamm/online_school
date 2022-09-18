from rest_framework import serializers
from .models import Classes, Course, TimeTable
from .messages import *


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'


class TimeTableSerializer(serializers.ModelSerializer):
    _class_ = serializers.UUIDField()

    class Meta:
        model = TimeTable
        exclude = ['_class']

    def validate(self, data):
        _days = data.get('days')
        _start_time = data.get('start_time')
        _end_time = data.get('end_time')
        _room_no = data.get('room_no')
        _class = data.get('_class_')
        is_class_exists = Classes.objects.filter(id=_class).exists()

        if not is_class_exists:
            raise serializers.ValidationError(no_class_found(_class))

        if _start_time > _end_time:
            raise serializers.ValidationError(INVALID_TIME_MESSAGE)

        clash = TimeTable.objects.filter(start_time__lt=_end_time,
                                         end_time__gt=_start_time,
                                         room_no=_room_no,
                                         days=_days).exists()

        if clash:
            raise serializers.ValidationError(
                timetable_clash_message(_room_no))

        timetable: TimeTable = TimeTable.objects.create(
            days=_days,
            start_time=_start_time,
            end_time=_end_time,
            room_no=_room_no,
            _class=Classes.objects.get(id=_class)
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

        course = Course.objects.filter(course_code=course_code).exists()

        if not course:
            raise serializers.ValidationError(NO_COURSE_ERROR_MESSAGE)

        course_id = Course.objects.get(course_code=course_code).id

        # make sure that the class with the same course and section doesnot
        # exists
        is_class_already_registered = Classes.objects.filter(
            course_id=course_id, section=section).exists()

        if is_class_already_registered:
            raise serializers.ValidationError(CLASS_ALREADY_REGISTERED)

        teacher = self.context.get('teacher')
        classes: Classes = Classes.objects.create(
            enrollment_start_date=enrollment_start_date,
            enrollment_end_date=enrollment_end_date,
            teacher=teacher,
            section=section,
            course=Course.objects.get(course_code=course_code)
        )

        classes.save()

        return data
