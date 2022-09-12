import json
from unittest.mock import patch

import pytest
from accounts.messages import *
from accounts.models import Admin
from django.urls import reverse

url = reverse('Admin_Register')
pytestmark = pytest.mark.django_db

FIELD_REQUIRED_MESSAGE = {
    "errors": {
        "email": [
            "This field is required."
        ],
        "name": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ],
        "password2": [
            "This field is required."
        ]}
}

DATA = {'name': 'Admin', 'email': 'admin@test.com', 'password': '1234',
        'password2': '1234'}

DUMMY_TOKEN = {
    "refresh": "DummyRefreshToken",
    "access": "DummyAccessToken"
}


def test_admin_get_zero_content(client):
    response = client.post(url)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client):
    DATA['password2'] = "12345"
    response = client.post(url, DATA)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"errors": {
        "non_field_errors": [
            PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH
        ]}
    }


def test_admin_with_same_email(client):
    Admin.objects.create_user(name='Admin', email='admin@test.com')
    response = client.post(url, DATA)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"errors": {
        "email": [
            "user with this Email already exists."
        ]
    }
    }


def test_admin_with_wrong_data(client):
    DATA['email'] = "admintest.com"
    response = client.post(url, DATA)

    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"errors": {
        "email": [
            "Enter a valid email address."
        ]}
    }


@pytest.mark.xfail
@patch('accounts.views.get_tokens_for_user')
def test_admin_registeration_success(patch_token, client):
    patch_token.return_value = DUMMY_TOKEN

    response = client.post(url, DATA)
    response_content = json.loads(response.content)

    assert response_content == {
        "msg": REGISTERATION_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN
    }
    assert response.status_code == 201
