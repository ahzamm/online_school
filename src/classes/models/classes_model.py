from uuid import uuid4

from accounts.models import Teacher
from classes.models.course_model import Course
from django.db import models
from django.utils.text import slugify


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
