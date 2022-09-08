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
    return response_content['token']['access']


@pytest.fixture
def create_test_student(client, create_test_admin):
    data = {
        "email": "student@test.com",
        "name": "Student",
        "password": "1234",
        "password2": "1234"
    }
    token = create_test_admin
    response = client.post(reverse("Student_Register"),
                           data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    return response_content['token']['access']


@pytest.fixture
@patch('accounts.views.get_tokens_for_user')
def admin_login(patch_token, client, **kwargs):
    def _admin_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
        data = {
            "email": email,
            "password": password
        }
        response = client.post(reverse('Admin_Login'), data)
        return response
    return _admin_login


@pytest.fixture
@patch('accounts.views.get_tokens_for_user')
def teacher_login(patch_token, client, **kwargs):
    def _teacher_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
        data = {
            "email": email,
            "password": password
        }
        response = client.post(reverse('Teacher_Login'), data)
        return response
    return _teacher_login


@pytest.fixture
@patch('accounts.views.get_tokens_for_user')
def student_login(patch_token, client, **kwargs):
    def _student_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
        data = {
            "email": email,
            "password": password
        }
        response = client.post(reverse('Student_Login'), data)
        return response
    return _student_login
