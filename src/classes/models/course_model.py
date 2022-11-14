from uuid import uuid4

from django.db import models
from django.utils.text import slugify


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
