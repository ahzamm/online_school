import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from accounts.messages import *
from accounts.models import Teacher
from django.urls import reverse

from .extra import FIELD_REQUIRED_MESSAGE, non_field_error

url = reverse('Teacher_Register')
pytestmark = pytest.mark.django_db


_DATA = {'name': 'Admin', 'email': 'teacher@test.com',
         'password': '1234', 'password2': '1234'}


def test_get_zero_content(client, create_test_admin):
    token = create_test_admin

    response = client.post(
        url,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client,
                                create_test_admin):
    DATA = deepcopy(_DATA)
    DATA['password2'] = "12345"
    token = create_test_admin

    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)


def test_with_same_email(client, create_test_admin):
    DATA = deepcopy(_DATA)

    Teacher.objects.create(name='Admin',
                           email='teacher@test.com')

    token = create_test_admin
    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "user with this Email already exists.",
        ]},
    }


def test_with_wrong_data(client, create_test_admin):
    DATA = deepcopy(_DATA)
    DATA['email'] = "teachertest.com"
    token = create_test_admin

    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "Enter a valid email address.",
        ]},
    }


@patch('accounts.views.teacher_views.get_tokens_for_user')
def test_registeration_success(patch_token, client,
                               create_test_admin):
    DATA = deepcopy(_DATA)
    patch_token.return_value = {
        "refresh": "DummyRefreshToken",
        "access": "DummyAccessToken",
    }
    token = create_test_admin

    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 201
    assert response_content == {
        "msg": "Registeration Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken",
        },
    }
