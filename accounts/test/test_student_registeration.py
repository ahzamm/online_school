import json
from copy import deepcopy
from unittest.mock import patch
import pytest
from django.urls import reverse

from accounts.messages import (
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    REGISTERATION_SUCCESS_MESSAGE,
)
from accounts.models import Student

from .extra import DUMMY_TOKEN, STUDENT_FIELD_REQUIRED_MESSAGE, non_field_error

url = reverse("student:Student_Register")
pytestmark = pytest.mark.django_db


_DATA = {
    "name": "Student",
    "roll_no": "roll_no_1",
    "email": "student@test.com",
    "password": "1234",
    "password2": "1234",
}


def test_get_zero_content(client, create_test_admin):

    # arrange
    token = create_test_admin

    response = client.post(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == STUDENT_FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    data["password2"] = "123456"
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    )


def test_with_same_email(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    Student.objects.create(name="Admin", email="student@test.com")
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "user with this Email already exists.",
            ],
        },
    }


def test_with_wrong_data(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    data["email"] = "studenttest.com"
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "Enter a valid email address.",
            ],
        },
    }


@patch("accounts.views.student_views.get_tokens_for_user")
def test_registeration_success(patch_token, client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    patch_token.return_value = DUMMY_TOKEN
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 201
    assert json.loads(response.content) == {
        "msg": REGISTERATION_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN,
    }
