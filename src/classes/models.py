from uuid import uuid4

from django.db import models
from django.utils.text import slugify

from accounts.models import Student, Teacher


class Course(models.Model):
    class CH(models.IntegerChoices):
        THREE = 3
        FOUR = 4

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    name = models.CharField(max_length=50, null=False, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    course_code = models.CharField(max_length=50, null=False, unique=True)
    ch = models.IntegerField(choices=CH.choices)
    pre_req_courses = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="pre_req",
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}"

    def __str__(self):
        return str(self.name)


class Classes(models.Model):
    class SECTION(models.TextChoices):
        A = "A"
        B = "B"
        C = "C"

    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
        unique=True,
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )
    teacher = models.ForeignKey(
        Teacher,
        null=True,
        on_delete=models.CASCADE,
        related_name="teacher",
    )
    slug = models.SlugField(max_length=100, null=True, blank=True)
    student = models.ManyToManyField(
        "accounts.Student",
        blank=True,
        # related_name="student",
    )
    enrollment_start_date = models.DateField()
    enrollment_end_date = models.DateField()
    section = models.CharField(
        max_length=1,
        choices=SECTION.choices,
    )

    mid_exammination_date = models.DateField(
        null=True,
    )
    final_exammination_date = models.DateField(
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.course.name}_{self.section}")
        super(Classes, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}"

    def __str__(self):
        return str(f"{self.course}....{self.section}")


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
