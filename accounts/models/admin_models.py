
from uuid import uuid4

from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from .user_models import User


class AdminManager(BaseUserManager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.ADMIN)

    def create_user(self, email=None, name=None, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            type=User.Type.ADMIN
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class Admin(User):

    objects = AdminManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)
