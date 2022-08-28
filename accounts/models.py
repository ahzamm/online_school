"""create our models here."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    """Create custom User model."""

    class Type(models.TextChoices):
        """Choices for our user default: Admin."""

        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'
        ADMIN = "ADMIN", 'Admin'

    type = models.CharField(_('Type'), max_length=50,
                            choices=Type.choices, default=Type.ADMIN)

    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    # def get_absolute_url(self):
    #     return reverse("user:detail", kwargs={"username": self.username})

    # def user_greet(self):
    #     return "Hi from USER"


class AdminManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.ADMIN)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.ADMIN


class TeacherManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.TEACHER)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.TEACHER


class StudentManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.STUDENT)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.STUDENT


class StudentMore(models.Model):
    class Grade(models.TextChoices):
        ONE = 'One'
        TWO = 'Two'
        THREE = 'Three'
        FOURE = 'Foure'
        FIVE = 'Five'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(_('Grade'), max_length=50,
                             choices=Grade.choices)


class Admin(User):
    """Model for our database admin."""

    objects = AdminManager()

    class Meta:
        proxy = True

    def admin_greet(self):
        return "Hi from ADMIN"


class Teacher(User):
    """Model for our Teachers."""

    objects = TeacherManager()

    class Meta:
        proxy = True


class Student(User):
    """Model for our Students."""

    objects = StudentManager()

    class Meta:
        proxy = True

    @property
    def more(self):
        return self.studentmore
