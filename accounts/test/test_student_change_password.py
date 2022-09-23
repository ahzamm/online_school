
import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from accounts.messages import (PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
                               WRONG_OLD_PASSWORD)
from django.urls import reverse

from .extra import DUMMY_TOKEN, non_field_error

url = reverse('Student_Change_Password')
pytestmark = pytest.mark.django_db

_DATA = {"old_password": "1234",
         "password": "12345",
         "password2": "12345"}


def test_student_change_wrong_old_password(client,
                                           create_test_student):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_student
    data["old_password"] = "123"

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(WRONG_OLD_PASSWORD)


def test_wrong_confirm_password(client, create_test_student):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_student
    data["password2"] = "123456"

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)


@patch('accounts.views.student_views.get_tokens_for_user')
def test_change_password_success(patch_token, client,
                                 create_test_student, student_login):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_student
    response = client.post(
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    response = student_login(  # act
        patch_token=patch_token,
        client=client,
        email="student@test.com",
        password="12345",
    )

    # assert
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "msg": "Login Success",
        "token": DUMMY_TOKEN,
    }
