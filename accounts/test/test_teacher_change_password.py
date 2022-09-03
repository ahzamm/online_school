
from distutils.log import error
import json

import jwt
import pytest
from django.urls import reverse
from school import settings

url = reverse('Teacher_Change_Password')
pytestmark = pytest.mark.django_db


def test_teacher_change_wrong_old_password(client, create_test_teacher):
    token = create_test_teacher

    data = {
        "old_password": "123",
        "password": "12345",
        "password2": "12345",
    }
    error_message = {
        "errors": {
            "non_field_errors": [
                "Wrong old Password"
            ]
        }
    }
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == error_message


def test_wrong_confirm_password(client, create_test_teacher):
    token = create_test_teacher

    data = {
        "old_password": "1234",
        "password": "12345",
        "password2": "123456",
    }
    error_message = {
        "errors": {
            "non_field_errors": [
                "Password and Confirm Password doesn't match"
            ]
        }
    }
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == error_message


def test_change_password_success(client, create_test_teacher):
    token = create_test_teacher

    data = {
        "old_password": "1234",
        "password": "12345",
        "password2": "12345",
    }
    message = {
        "msg": "password changed successfully"
    }
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == message
