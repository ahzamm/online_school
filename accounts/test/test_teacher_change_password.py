
import json
from unittest.mock import patch

import pytest
from django.urls import reverse

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


@patch('accounts.views.get_tokens_for_user')
def test_change_password_success(patch_token, client, create_test_teacher, teacher_login):

    # == == == == == == == == Test Change Password == == == == == == == ==

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

    # == == == == == == == == Test Login With Changed Password == == == == == == == ==

    response = teacher_login(patch_token=patch_token,
                             client=client, email="teacher@test.com", password="12345")
    response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content == {
        "msg": "Login Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
    }
