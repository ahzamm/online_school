
from django.contrib.auth.models import BaseUserManager
from django.db import models

from .user_models import User


class TeacherManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.TEACHER)

    def create_user(self, email=None, name=None, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            type=User.Type.TEACHER
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class TeacherMore(models.Model):
    salary = models.IntegerField()


class Teacher(User):
    """Model for our Teachers."""

    objects = TeacherManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.TEACHER
        return super().save(*args, **kwargs)

    @property
    def more(self):
        return self.teachermore
