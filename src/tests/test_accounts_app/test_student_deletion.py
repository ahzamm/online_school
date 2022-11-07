import json
from accounts.models import Student
import pytest
from django.urls import reverse

url = reverse("student:StudentDelete", kwargs={"slug": "roll_no_1"})
pytestmark = pytest.mark.django_db


def test_student_deletion_success(
    client,
    create_test_student,
    create_test_admin,
):
    token = create_test_admin

    assert Student.objects.all().count() == 1

    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "msg": "Student deleted successfully",
    }


def test_student_deletion_notfound(client, create_test_admin):
    token = create_test_admin
    assert Student.objects.all().count() == 0

    response = client.delete(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {"msg": "Student not Found"}
