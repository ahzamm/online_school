import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from accounts.messages import EMAIL_PASSWORD_NOT_VALID_MESSAGE
from accounts.models import Teacher
from django.urls import reverse

from .extra import DUMMY_TOKEN, non_field_error

url = reverse("Teacher_Login")
pytestmark = pytest.mark.django_db

_DATA = {
    "email": "teacher@test.com",
    "password": "1234",
}


def test_login_with_no_data(client):
    response = client.post(url)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "This field is required.",
            ],
            "password": [
                "This field is required.",
            ],
        },
    }


def test_wrong_email_password(client):

    # arrange
    data = deepcopy(_DATA)

    response = client.post(url, data)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        EMAIL_PASSWORD_NOT_VALID_MESSAGE
    )


@patch("accounts.views.teacher_views.get_tokens_for_user")
def test_login_success(patch_token, client):

    # arrange
    data = deepcopy(_DATA)
    patch_token.return_value = DUMMY_TOKEN
    Teacher.objects.create_user(
        name="Teacher",
        email="teacher@test.com",
        password="1234",
    )

    response = client.post(url, data)  # act

    assert response.status_code == 200
    assert json.loads(response.content) == {
        "msg": "Login Success",
        "token": DUMMY_TOKEN,
    }
