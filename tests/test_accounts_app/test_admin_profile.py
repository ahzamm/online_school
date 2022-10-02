import json
from copy import deepcopy

import jwt
import pytest
from django.urls import reverse

from school import settings

url = reverse("student:Admin_Profile")
pytestmark = pytest.mark.django_db

_DATA = {
    "id": "user_id",
    "email": "admin@test.com",
    "name": "Admin",
}


def test_admin_profile(client, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
    )
    user_id = payload.get("user_id")
    data["id"] = user_id

    response = client.get(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 200
    assert json.loads(response.content) == data


def test_no_admin_profile(client, create_test_teacher):
    # arrange
    token = create_test_teacher
    error_message = {
        "errors": {
            "detail": "You do not have permission to perform this action.",
        },
    }

    response = client.get(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert response.status_code == 403
    assert json.loads(response.content) == error_message
