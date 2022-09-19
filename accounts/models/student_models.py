
from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .user_models import User


class StudentManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.STUDENT)

    def create_user(self, email=None, name=None, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            type=User.Type.STUDENT
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


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
