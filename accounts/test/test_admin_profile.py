
import json
from copy import deepcopy

import jwt
import pytest
from django.urls import reverse
from school import settings

url = reverse('Admin_Profile')
pytestmark = pytest.mark.django_db

_DATA = {
    "id": "user_id",
    "email": "admin@test.com",
    "name": "Admin",
}


def test_admin_profile(client, create_test_admin):
    DATA = deepcopy(_DATA)
    token = create_test_admin

    payload = jwt.decode(token, settings.SECRET_KEY,
                         algorithms=['HS256'])

    user_id = payload.get('user_id')

    DATA["id"] = user_id
    response = client.get(url,
                          **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == DATA


def test_no_admin_profile(client, create_test_teacher):
    token = create_test_teacher

    response = client.get(
        url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    response_content = json.loads(response.content)

    error_message = {
        "errors": {
            "detail": "You do not have permission to perform this action.",
        },
    }

    assert response_content == error_message
    assert response.status_code == 403
