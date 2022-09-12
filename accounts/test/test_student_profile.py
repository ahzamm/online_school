
import json

import jwt
import pytest
from django.urls import reverse
from school import settings

url = reverse('Student_Profile')
pytestmark = pytest.mark.django_db

DATA = {
    "id": "user_id",
    "email": "student@test.com",
    "name": "Student"
}


def test_student_profile(client, create_test_student):

    token = create_test_student

    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=['HS256'])

    user_id = payload.get('user_id')

    DATA["id"] = user_id
    response = client.get(
        url, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    assert response.status_code == 200
    assert response_content == DATA


def test_no_student_profile(client, create_test_admin):
    token = create_test_admin

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
