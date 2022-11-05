import json

import pytest
from django.urls import reverse

url = reverse("student:ListAllTeacher")
pytestmark = pytest.mark.django_db


def test_list_no_student_detail(client, create_test_admin):
    """
    Check the response when no teacher is present in out database
    """
    token = create_test_admin

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "count": 0,
        "next": None,
        "previous": None,
        "results": [],
    }


def test_list_all_teacher(
    client,
    create_test_teacher_with_kwargs,
    create_test_admin,
):
    token = create_test_admin
    create_test_teacher_with_kwargs(
        client=client,
        email="test1@example.com",
        name="Test 1",
        tea_id="teacher_no_1",
        password="password1234",
        password2="password1234",
    )
    create_test_teacher_with_kwargs(
        client=client,
        email="test2@example.com",
        name="Test 3",
        tea_id="teacher_no_2",
        password="password1234",
        password2="password1234",
    )

    response = client.get(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "count": 2,
        "next": None,
        "previous": None,
        "results": [
            {
                "tea_id": "teacher_no_1",
                "teacher_detail": "http://testserver/api/account/teachers/teacher_no_1/",
            },
            {
                "tea_id": "teacher_no_2",
                "teacher_detail": "http://testserver/api/account/teachers/teacher_no_2/",
            },
        ],
    }
