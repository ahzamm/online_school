from rest_framework import serializers

from ..messages import (
    INVALID_TIME_MESSAGE,
    no_class_found,
    timetable_clash_message,
)
from ..models import Classes, TimeTable
from .classes_serializer import ListAllClassesSerializer


class TimeTableSerializer(serializers.ModelSerializer):
    _class_ = serializers.UUIDField()

    class Meta:
        model = TimeTable
        exclude = ["_class"]

    def validate(self, data):
        days = data.get("days")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        room_no = data.get("room_no")
        _class = data.get("_class_")
        is_class_exists = Classes.objects.filter(id=_class).exists()

        if not is_class_exists:
            raise serializers.ValidationError(no_class_found(_class))

        if start_time > end_time:
            raise serializers.ValidationError(INVALID_TIME_MESSAGE)

        if TimeTable.objects.filter(
            start_time__lt=end_time,
            end_time__gt=start_time,
            room_no=room_no,
            days=days,
        ).exists():

            raise serializers.ValidationError(timetable_clash_message(room_no))

        timetable: TimeTable = TimeTable.objects.create(
            days=days,
            start_time=start_time,
            end_time=end_time,
            room_no=room_no,
            _class=Classes.objects.get(id=_class),
        )

        timetable.save()

        return data


class PureTimeTableSerializer(serializers.ModelSerializer):
    _class = ListAllClassesSerializer(read_only=True)

    class Meta:
        model = TimeTable
        exclude = ["id"]
