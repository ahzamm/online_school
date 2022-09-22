
import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from accounts.messages import *
from django.urls import reverse

from .extra import DUMMY_TOKEN, non_field_error

url = reverse('Teacher_Change_Password')
pytestmark = pytest.mark.django_db

_DATA = {"old_password": "1234",
         "password": "12345",
         "password2": "12345"}


def test_teacher_change_wrong_old_password(client, create_test_teacher):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher
    data["old_password"] = "123"

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'
           }
    )

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(WRONG_OLD_PASSWORD)


def test_wrong_confirm_password(client, create_test_teacher):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher
    data["password2"] = "123456"

    response = client.post(url, data,  # act
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    # assert
    assert response.status_code == 400
    assert json.loads(response.content) == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH)


@patch('accounts.views.teacher_views.get_tokens_for_user')
def test_change_password_success(patch_token, client,
                                 create_test_teacher, teacher_login):
    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher
    response = client.post(url, data,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    response = teacher_login(  # act
        patch_token=patch_token,
        client=client,
        email="teacher@test.com",
        password="12345"
    )

    # assert
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "msg": LOGIN_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN,
    }
