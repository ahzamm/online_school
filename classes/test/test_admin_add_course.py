import pytest
from django.urls import reverse
import json

url = reverse('CourseRegisteration')
pytestmark = pytest.mark.django_db


def test_teacher_create_course(client, create_test_teacher):
    token = create_test_teacher
    data = {"name": "Test Course", "course_code": "TC123",
            "ch": "4", "email": "teacher@test.com"}
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    error_message = {'errors': {
        'detail': 'You do not have permission to perform this action.'}}
    assert response_content == error_message


def test_create_course_with_wrong_email(client, create_test_admin):
    token = create_test_admin
    data = {"name": "Test Course", "course_code": "TC123",
            "ch": "4", "email": "teacher@test.com"}
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    error_message = {'errors': {'non_field_errors': [
        'No teacher with this email found']}}
    assert response_content == error_message


def test_admin_create_course_success(client, create_test_admin, create_test_teacher):
    token = create_test_admin
    data = {"name": "Test Course", "course_code": "TC123",
            "ch": "4", "email": "teacher@test.com"}
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    success_message = {'msg': 'COURSE ADDED SUCCESSFULLY'}
    assert response_content == success_message
