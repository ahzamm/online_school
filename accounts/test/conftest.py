import json
from unittest.mock import patch
import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db


@pytest.fixture
def create_test_admin(client):
    data = {
        "email": "admin@test.com",
        "name": "Admin",
        "password": "1234",
        "password2": "1234"
    }
    response = client.post(reverse("Admin_Register"), data)
    response_content = json.loads(response.content)
    print("=====>", response_content)
    return response_content['token']['access']


@pytest.fixture
def create_test_teacher(client, create_test_admin):
    data = {
        "email": "teacher@test.com",
        "name": "Teacher",
        "password": "1234",
        "password2": "1234"
    }
    token = create_test_admin
    response = client.post(
        reverse("Teacher_Register"), data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    print("=====>", response_content)
    return response_content['token']['access']


@ pytest.fixture
def create_test_student(client):
    data = {
        "email": "student@test.com",
        "name": "Student",
        "password": "1234",
        "password2": "1234"
    }
    response = client.post(reverse("Student_Register"), data)
    response_content = json.loads(response.content)
    return response_content['token']['access']
