import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from django.urls import reverse

from accounts.messages import (
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    REGISTERATION_SUCCESS_MESSAGE,
)
from accounts.models import Admin

from .extra import DUMMY_TOKEN, FIELD_REQUIRED_MESSAGE, non_field_error

url = reverse("student:StudentDetail", kwargs={"slug": "roll_no_43"})
pytestmark = pytest.mark.django_db


def test_list_no_student_detail(client):
    """
    Check the response when no student is present in out database / wrong slug
    """
    response = client.get(url)  # act

    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.xfail()
def test_list_one_student(client, create_test_student_with_kwargs):
    create_test_student_with_kwargs(
        client=client,
        email="test1@example.com",
        name="Test",
        roll_no="Roll_No_43",
        password="password1234",
        password2="password1234",
    )

    response = client.get(url)  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "cleared_course": [],
        "email": "test1@example.com",
        "enrolled_classes": [],
        "grade": "",
        "name": "Test",
        "roll_no": "Roll_No_43",
    }
