import json
from unittest.mock import patch
from accounts.messages import *
import pytest
from accounts.models import Admin
from django.urls import reverse
from .extra import non_field_error

url = reverse('Admin_Login')
pytestmark = pytest.mark.django_db

DATA = {'email': 'admin@test.com', 'password': '1234'}

DUMMY_TOKEN = {
    "refresh": "DummyRefreshToken",
    "access": "DummyAccessToken"
}


def test_login_with_no_data(client):
    response = client.post(url)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {"errors": {"email": ["This field is required."],
                                "password": ["This field is required."]}}


def test_wrong_email_password(client):

    response = client.post(url, DATA)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == non_field_error(
        EMAIL_PASSWORD_NOT_VALID_MESSAGE)


@patch('accounts.views.get_tokens_for_user')
def test_login_success(patch_token, client):
    patch_token.return_value = DUMMY_TOKEN

    Admin.objects.create_user(
        name="Admin", email="admin@test.com", password="1234")

    response = client.post(url, DATA)
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == {
        "msg": LOGIN_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN
    }
