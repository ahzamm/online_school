from uuid import uuid4

from accounts.models import Student
from classes.models.classes_model import Classes
from django.db import models


class Attendence(models.Model):
    class Status(models.TextChoices):
        PRESENT = "P"
        ABSENT = "A"

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    _class = models.ForeignKey(
        Classes,
        on_delete=models.CASCADE,
    )
    student = models.ManyToManyField(Student, default=None)
    status = models.CharField(
        max_length=5,
        choices=Status.choices,
        default=Status.ABSENT,
    )

    def __str__(self):
        return str(self._class)
