import json

import pytest
from django.urls import reverse

url = reverse("student:ListAllStudent")
pytestmark = pytest.mark.django_db


def test_list_no_student_detail(client, create_test_admin):
    """
    Check the response when no student is present in out database
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


def test_list_all_student(
    client,
    create_test_student_with_kwargs,
    create_test_admin,
):
    token = create_test_admin
    create_test_student_with_kwargs(
        client=client,
        email="test1@example.com",
        name="Test 1",
        roll_no="Roll_No_1",
        password="password1234",
        password2="password1234",
    )
    create_test_student_with_kwargs(
        client=client,
        email="test2@example.com",
        name="Test 3",
        roll_no="Roll_No_2",
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
                "roll_no": "Roll_No_1",
                "student_detail": "http://testserver/api/account/students/roll_no_1/",
            },
            {
                "roll_no": "Roll_No_2",
                "student_detail": "http://testserver/api/account/students/roll_no_2/",
            },
        ],
    }
