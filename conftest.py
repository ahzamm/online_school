import json
from unittest.mock import patch

import pytest
from django.urls import reverse
from classes.models import Classes

pytestmark = pytest.mark.django_db


@pytest.fixture
def create_test_admin(client):
    data = {
        "email": "admin@test.com",
        "name": "Admin",
        "password": "1234",
        "password2": "1234",
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
        "password2": "1234",
    }
    token = create_test_admin
    response = client.post(
        reverse("Teacher_Register"), data, **{'HTTP_AUTHORIZATION':
                                              f'Bearer {token}'})
    response_content = json.loads(response.content)

    return response_content['token']['access']


@pytest.fixture
def create_test_student(client, create_test_admin):
    data = {
        "email": "student@test.com",
        "name": "Student",
        "password": "1234",
        "password2": "1234",
    }
    token = create_test_admin
    response = client.post(reverse("Student_Register"), data,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    return response_content['token']['access']


@pytest.fixture
@patch('accounts.views.admin_views.get_tokens_for_user')
def admin_login(patch_token, client, **kwargs):
    def _admin_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken",
        }
        data = {
            "email": email,
            "password": password,
        }

        return client.post(reverse('Admin_Login'), data)

    return _admin_login


@pytest.fixture
@patch('accounts.views.teacher_views.get_tokens_for_user')
def teacher_login(patch_token, client, **kwargs):
    def _teacher_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken",
        }
        data = {
            "email": email,
            "password": password,
        }

        return client.post(reverse('Teacher_Login'), data)

    return _teacher_login


@pytest.fixture
@patch('accounts.views.student_views.get_tokens_for_user')
def student_login(patch_token, client, **kwargs):
    def _student_login(client, patch_token, **kwargs):
        email = kwargs.pop("email")
        password = kwargs.pop("password")
        patch_token.return_value = {
            "refresh": "DummyRefreshToken",
            "access": "DummyAccessToken",
        }
        data = {
            "email": email,
            "password": password,
        }

        return client.post(reverse('Student_Login'), data)

    return _student_login


@pytest.fixture
def create_test_course(client, create_test_admin, create_test_teacher):
    data = {
        "name": "Test Course",
        "course_code": "TC123",
        "ch": "4",
    }
    token = create_test_admin

    response = client.post(reverse("CourseRegisteration"), data,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    return json.loads(response.content)


@pytest.fixture
def create_test_class(client, create_test_teacher, create_test_course):
    data = {
        "course_code": "TC123",
        "enrollment_start_date": "2022-04-14",
        "enrollment_end_date": "2022-04-18",
        "section": "A",
    }

    token = create_test_teacher
    response = client.post(reverse("ClassRegister"), data,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    return json.loads(response.content)


@pytest.fixture
def create_test_timetable(client, create_test_class, create_test_admin):
    token = create_test_admin
    test_class = Classes.objects.first()
    test_class_id = test_class.id

    data = {"days": "MONDAY",
            "start_time": "09:30:00",
            "end_time": "10:45:00",
            "_class_": test_class_id,
            "room_no": "ROOM_3"}

    response = client.post(reverse('TimeTableRegisteration'), data,
                           **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    return json.loads(response.content)
