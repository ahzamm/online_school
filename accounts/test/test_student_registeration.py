import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from accounts.messages import *
from accounts.models import Student
from django.urls import reverse

from .extra import DUMMY_TOKEN, FIELD_REQUIRED_MESSAGE, non_field_error

url = reverse('Student_Register')
pytestmark = pytest.mark.django_db


_DATA = {'name': 'Student', 'email': 'student@test.com',
         'password': '1234', 'password2': '1234'}


def test_get_zero_content(client, create_test_admin):
    token = create_test_admin

    response = client.post(url,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client, create_test_admin):
    DATA = deepcopy(_DATA)

    DATA['password2'] = "123456"
    token = create_test_admin

    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 400
    assert response_content == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)


def test_with_same_email(client, create_test_admin):
    DATA = deepcopy(_DATA)
    Student.objects.create(name='Admin', email='student@test.com')
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
    DATA['email'] = "studenttest.com"
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


@patch('accounts.views.student_views.get_tokens_for_user')
def test_registeration_success(patch_token, client, create_test_admin):
    DATA = deepcopy(_DATA)
    patch_token.return_value = DUMMY_TOKEN
    token = create_test_admin

    response = client.post(url, DATA,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response_content == {"msg": REGISTERATION_SUCCESS_MESSAGE,
                                "token": DUMMY_TOKEN}
    assert response.status_code == 201
