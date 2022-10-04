import pytest
from django.urls import reverse

url = reverse("course:CourseDetail")
pytestmark = pytest.mark.django_db
