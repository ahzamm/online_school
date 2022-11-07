import json

import pytest
from classes.models import Course
from django.urls import reverse

url = reverse("course:CourseDelete", kwargs={"slug": "test-course"})
pytestmark = pytest.mark.django_db


def test_course_delete_success(client, create_test_course, create_test_admin):
    token = create_test_admin
    assert Course.objects.all().count() == 1

    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "msg": "Course deleted successfully",
    }


def test_course_deletion_notfound(client, create_test_admin):
    token = create_test_admin
    assert Course.objects.all().count() == 0
    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {"msg": "Course not Found"}
