
import json
from unittest.mock import patch
from accounts.messages import *
import pytest
from django.urls import reverse
from .extra import non_field_error

url = reverse('Student_Change_Password')
pytestmark = pytest.mark.django_db

DATA = {
    "old_password": "1234",
    "password": "12345",
    "password2": "12345",
}

DUMMY_TOKEN = {
    "refresh": "DummyRefreshToken",
    "access": "DummyAccessToken"
}


def test_student_change_wrong_old_password(client, create_test_student):
    token = create_test_student

    DATA["old_password"] = "123"

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == non_field_error(WRONG_OLD_PASSWORD)


def test_wrong_confirm_password(client, create_test_student):
    token = create_test_student

    DATA["password2"] = "123456"

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)


@pytest.mark.xfail
@patch('accounts.views.get_tokens_for_user')
def test_change_password_success(patch_token, client, create_test_student, student_login):
    # == == == == == == == == Test Change Password == == == == == == == ==
    token = create_test_student

    message = {
        "msg": PASSWORD_CHANGE_SUCCESS_MESSAGE
    }
    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == message

    # == == == == == == == == Test Login With Changed Password == == == == == == == ==

    response = student_login(patch_token=patch_token,
                             client=client, email="student@test.com", password="12345")
    response.status_code == 200
    response_content = json.loads(response.content)
    assert response_content == {
        "msg": "Login Success",
        "token": DUMMY_TOKEN
    }
