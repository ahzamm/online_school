import pytest
from django.urls import reverse
import json
from classes.messages import *

url = reverse('CourseRegisteration')
pytestmark = pytest.mark.django_db

DATA = {"name": "Test Course", "course_code": "TC123",
        "ch": "4", "email": "teacher@test.com"}


def test_teacher_create_course(client, create_test_teacher):
    token = create_test_teacher

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    error_message = {'errors': {
        'detail': 'You do not have permission to perform this action.'}}
    assert response_content == error_message


def test_create_course_with_wrong_email(client, create_test_admin):
    token = create_test_admin

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    error_message = {'errors': {
        'non_field_errors': [NO_TEACHER_FOUND_MESSAGE]}}
    assert response_content == error_message


def test_admin_create_course_success(client, create_test_admin, create_test_teacher):
    token = create_test_admin

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    success_message = {'msg': COURSE_REGISTER_SUCCESS_MESSAGE}
    assert response_content == success_message
