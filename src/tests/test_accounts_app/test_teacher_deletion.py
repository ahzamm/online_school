import json

import pytest
from accounts.models import Teacher
from django.urls import reverse

url = reverse("student:TeacherDelete", kwargs={"slug": "teacher_no_1"})
pytestmark = pytest.mark.django_db


def test_teacher_deletion_success(
    client,
    create_test_teacher,
    create_test_admin,
):
    token = create_test_admin

    assert Teacher.objects.all().count() == 1

    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "msg": "Teacher deleted successfully",
    }


def test_teacher_deletion_notfound(client, create_test_admin):
    token = create_test_admin
    assert Teacher.objects.all().count() == 0

    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {"msg": "Teacher not Found"}
