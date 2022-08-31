import json
from unittest.mock import patch

import pytest
from accounts.models import Student
from django.urls import reverse

url = reverse('Student_Register')
pytestmark = pytest.mark.django_db

FIELD_REQUIRED_MESSAGE = {
    'errors': {
        "email": [
            "This field is required."
        ],
        "name": [
            "This field is required."
        ],
        "password": [
            "This field is required."
        ],
        "password2": [
            "This field is required."
        ]}
}


def test_get_zero_content(client):
    response = client.post(url)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == FIELD_REQUIRED_MESSAGE


def test_wrong_confirm_password(client):
    data = {
        'name': 'Student', 'email': 'student@test.com', 'password': '1234',
        'password2': '12345'}
    response = client.post(url, data)
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "non_field_errors": [
            "Password and Confirm Password doesn't match"
        ]}
    }


def test_with_same_email(client):
    Student.objects.create(name='Admin', email='student@test.com')
    response = client.post(url, {'name': 'Admin', 'email': 'student@test.com',
                                 'password': '1234', 'password2': '1234'})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "user with this Email already exists."
        ]}
    }


def test_with_wrong_data(client):
    response = client.post(url, {'name': 'Student', 'email': 'studenttest.com',
                                 'password': '1234', 'password2': '1234'})
    response_content = json.loads(response.content)
    assert response.status_code == 400
    assert response_content == {'errors': {
        "email": [
            "Enter a valid email address."
        ]}
    }


@patch('accounts.views.get_tokens_for_user')
def test_registeration_success(patch_token, client):
    patch_token.return_value = {
        "refresh": "DummyRefreshToken",
        "access": "DummyAccessToken"
    }
    data = {
        'name': 'Student',
        'email': 'student@example.com',
        'password': '1234',
        'password2': '1234'
    }
    response = client.post(url, data)
    response_content = json.loads(response.content)
    assert response.status_code == 201
    assert response_content == {
        "msg": "Registeration Success",
        "token": {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken"
        }
    }
