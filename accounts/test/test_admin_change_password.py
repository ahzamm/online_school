import json
from copy import deepcopy
from unittest.mock import patch

import pytest
from django.urls import reverse

from accounts.messages import (LOGIN_SUCCESS_MESSAGE,
                               PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH,
                               PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH_STATUS,
                               WRONG_OLD_PASSWORD, WRONG_OLD_PASSWORD_STATUS)

from .extra import DUMMY_TOKEN, non_field_error

url = reverse("Admin_Change_Password")
pytestmark = pytest.mark.django_db

_DATA = {
    "old_password": "1234",
    "password": "12345",
    "password2": "12345",
}


def test_admin_change_wrong_old_password(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    data["old_password"] = "123"

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == WRONG_OLD_PASSWORD_STATUS
    assert json.loads(response.content) == non_field_error(WRONG_OLD_PASSWORD)


def test_wrong_confirm_password(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    data["password2"] = "123456"

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH_STATUS
    assert json.loads(response.content) == non_field_error(
        PASSWORD_AND_CONFIRM_PASSWORD_NOT_MATCH
    )


@patch("accounts.views.admin_views.get_tokens_for_user")
def test_change_password_success(patch_token, client, create_test_admin, admin_login):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    response = client.post(
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    response = admin_login(  # act
        patch_token=patch_token,
        client=client,
        email="admin@test.com",
        password="12345",
    )

    # assert
    assert response.status_code == 200
    assert json.loads(response.content) == {
        "msg": LOGIN_SUCCESS_MESSAGE,
        "token": DUMMY_TOKEN,
    }
