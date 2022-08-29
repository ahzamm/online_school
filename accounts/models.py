"""create our models here."""
# TODO
# create seperate proxy model for admin
# make password compalsory for every user type


import uuid

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

#  Custom User Manager


class UserManager(BaseUserManager):
    def create(self, email, name, password=None, **kwargs):
        """
        Creates and saves a User with the given email, name, tc and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create(
            email,
            password=password,
            name=name,
        )
        user.type = User.Type.SUPER
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    class Type(models.TextChoices):
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'
        ADMIN = "ADMIN", 'Admin'
        SUPER = "SUPER", 'Super'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, unique=True)

    type = models.CharField(_('Type'), max_length=50,
                            choices=Type.choices, default=Type.SUPER)

    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class AdminManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.ADMIN)


class TeacherManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.TEACHER)


class StudentManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(
            type=User.Type.STUDENT)


class TeacherMore(models.Model):
    salary = models.IntegerField()


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
    """Model for our Teachers."""

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)


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


class Student(User):

    """Model for our Students."""

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
