from django.contrib.auth.models import BaseUserManager
from django.db import models
from .user_models import User
from django.utils.text import slugify


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.TEACHER)

    def create_user(self, email=None, name=None, password=None, **kwargs):

        if not email:
            raise ValueError("User must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            type=User.Type.TEACHER,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


class TeacherMore(models.Model):

    user = models.OneToOneField(
        "Teacher",
        related_name="teacher_more_info",
        on_delete=models.CASCADE,
    )
    tea_id = models.CharField(max_length=20, unique=True)
    salary = models.IntegerField(null=True)
    contact_number = models.IntegerField(null=True)
    degree = models.CharField(max_length=20, null=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tea_id)
        super(TeacherMore, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.slug}"


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
