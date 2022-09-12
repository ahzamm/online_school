import json
from unittest.mock import patch

import pytest
from accounts.messages import *
from accounts.models import Teacher
from django.urls import reverse

from .extra import DUMMY_TOKEN, non_field_error

url = reverse('Teacher_Login')
pytestmark = pytest.mark.django_db


def test_login_with_no_data(client):
    response = client.post(url)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"errors": {"email": ["This field is required."],
                                "password": ["This field is required."]}}


def test_wrong_email_password(client):
    data = {
        'email': 'teacher@test.com', 'password': '1234'}
    response = client.post(url, data)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == non_field_error(
        EMAIL_PASSWORD_NOT_VALID_MESSAGE)


@patch('accounts.views.get_tokens_for_user')
def test_login_success(patch_token, client):
    patch_token.return_value = DUMMY_TOKEN

    Teacher.objects.create_user(
        name="Teacher", email="teacher@test.com", password="1234")
    data = {"email": "teacher@test.com", "password": "1234"}
    response = client.post(url, data)
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == {
        "msg": "Login Success",
        "token": DUMMY_TOKEN
    }
