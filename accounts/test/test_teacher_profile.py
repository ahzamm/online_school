
import json

import jwt
import pytest
from django.urls import reverse
from school import settings

url = reverse('Teacher_Profile')
pytestmark = pytest.mark.django_db


def test_teacher_profile(client, create_test_teacher):

    token = create_test_teacher

    payload = jwt.decode(
        token, settings.SECRET_KEY,  algorithms=['HS256'])

    user_id = payload.get('user_id')

    data = {
        "id": user_id,
        "email": "teacher@test.com",
        "name": "Teacher"
    }
    response = client.get(
        url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == data


def test_no_teacher_profile(client, create_test_student):
    token = create_test_student

    response = client.get(
        url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    response_content = json.loads(response.content)

    error_message = {
        "errors": {
            "detail": "You do not have permission to perform this action."
        }
    }

    assert response_content == error_message
    assert response.status_code == 403
