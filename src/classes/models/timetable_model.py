from classes.models.classes_model import Classes
from django.db import models


class TimeTable(models.Model):
    class RoomNo(models.TextChoices):
        ROOM_1 = "ROOM_1"
        ROOM_2 = "ROOM_2"
        ROOM_3 = "ROOM_3"
        ROOM_4 = "ROOM_4"
        NOT_ANNOUNCED = "Not Announced Yet"

    class Days(models.TextChoices):
        MONDAY = "MONDAY"
        TUESDAY = "TUESDAY"
        WEDNESDAY = "WEDNESDAY"
        THURSDAY = "THURSDAY"
        FRIDAY = "FRIDAY"

    days = models.CharField(
        max_length=50,
        choices=Days.choices,
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_no = models.CharField(
        max_length=50,
        choices=RoomNo.choices,
        default=RoomNo.NOT_ANNOUNCED,
    )
    _class = models.ForeignKey(Classes, on_delete=models.CASCADE)

    def __str__(self):
        return f"{str(self._class)}.....{str(self.days)}"
