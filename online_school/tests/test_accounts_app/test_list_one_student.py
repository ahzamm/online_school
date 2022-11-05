import json

import pytest
from django.urls import reverse

url = reverse("student:StudentDetail", kwargs={"slug": "roll_no_43"})
pytestmark = pytest.mark.django_db


def test_list_no_student_detail(client, create_test_admin):
    """
    Check the response when no student is present in out database / wrong slug
    """
    token = create_test_admin

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    assert response.status_code == 404
    assert json.loads(response.content) == {"errors": {"detail": "Not found."}}


def test_list_one_student(
    client,
    create_test_student_with_kwargs,
    create_test_admin,
):
    create_test_student_with_kwargs(
        client=client,
        email="test1@example.com",
        name="Test",
        roll_no="Roll_No_43",
        password="password1234",
        password2="password1234",
    )
    token = create_test_admin

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "cleared_course": [],
        "email": "test1@example.com",
        "enrolled_classes": [],
        "grade": "",
        "name": "Test",
        "roll_no": "Roll_No_43",
    }


def test_differ_student(
    client,
    create_test_student,
    create_test_student_with_kwargs,
):
    """check the response when a student try to see detail of different student"""
    create_test_student_with_kwargs(
        client=client,
        email="test43@example.com",
        name="Test",
        roll_no="Roll_No_43",
        password="password1234",
        password2="password1234",
    )
    token = create_test_student

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    assert response.status_code == 400
    assert response.content == b'{"msg": "You do not have permission"}'
