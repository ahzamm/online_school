"""create our models here."""
# TODO
# create seperate proxy model for admin
# make password compalsory for every user type


from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

#  Custom User Manager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, password2=None):
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
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    class Type(models.TextChoices):
        STUDENT = "STUDENT", 'Student'
        TEACHER = "TEACHER", 'Teacher'
        ADMIN = "ADMIN", 'Admin'
        SUPER = "SUPER", 'Super'

    id = models.UUIDField(primary_key=True, default=uuid4,
                          editable=False, unique=True)

    type = models.CharField(_('Type'), max_length=50,
                            choices=Type.choices)

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
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


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

    objects = AdminManager()

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
