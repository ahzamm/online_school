from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .user_models import User


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return (
            super()
            .get_queryset(*args, **kwargs)
            .filter(
                type=User.Type.STUDENT,
            )
        )

    def create_user(self, email=None, name=None, password=None, **kwargs):

        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            type=User.Type.STUDENT,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class StudentMore(models.Model):
    class Grade(models.TextChoices):
        ONE = "One"
        TWO = "Two"
        THREE = "Three"
        FOURE = "Foure"
        FIVE = "Five"

    user = models.OneToOneField(
        "Student",
        related_name="more_info",
        on_delete=models.CASCADE,
    )
    roll_no = models.CharField(max_length=20, unique=True)
    grade = models.CharField(_("Grade"), max_length=50, choices=Grade.choices)
    cleared_course = models.ManyToManyField("classes.Course", blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.roll_no)
        super(StudentMore, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}"


class Student(User):

    objects = StudentManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):

        if not self.pk:
            self.type = User.Type.STUDENT
        return super().save(*args, **kwargs)

    @property
    def more(self):
        return self.studentmore
