import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from django.urls import reverse

from accounts.messages import (
    PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
    REGISTERATION_SUCCESS_MESSAGE,
)
from accounts.models import Admin

from .extra import DUMMY_TOKEN, FIELD_REQUIRED_MESSAGE, non_field_error

url = reverse("Admin_Register")
pytestmark = pytest.mark.django_db


_DATA = {
    "name": "Admin",
    "email": "admin@test.com",
    "password": "1234",
    "password2": "1234",
}


def test_admin_get_zero_content(client):

    response = client.post(url)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client):

    # arrange
    data = deepcopy(_DATA)
    data["password2"] = "12345"

    response = client.post(url, data)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH
    )


def test_admin_with_same_email(client):

    # arrange
    data = deepcopy(_DATA)
    Admin.objects.create_user(name="Admin", email="admin@test.com")

    response = client.post(url, data)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "user with this Email already exists.",
            ],
        },
    }


def test_admin_with_wrong_data(client):

    # arrange
    data = deepcopy(_DATA)
    data["email"] = "admintest.com"

    response = client.post(url, data)  # act

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == {
        "errors": {
            "email": [
                "Enter a valid email address.",
            ],
        },
    }


@patch("accounts.views.admin_views.get_tokens_for_user")
def test_admin_registeration_success(patch_token, client):

    # arrange
    data = deepcopy(_DATA)
    patch_token.return_value = DUMMY_TOKEN

    response = client.post(url, data)  # act

    # assert
    assert response.status_code == 201
    assert json.loads(response.content) == {
        "msg": REGISTERATION_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN,
    }
