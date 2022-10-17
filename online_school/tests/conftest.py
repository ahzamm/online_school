import json
from unittest.mock import patch

import pytest
from classes.models import Classes
from django.urls import reverse

pytestmark = pytest.mark.django_db

"""Fixtures without variables"""


@pytest.fixture()
def create_test_admin(client):
    data = {
        "email": "admin@test.com",
        "name": "Admin",
        "password": "1234",
        "password2": "1234",
    }
    response = client.post(reverse("student:Admin_Register"), data)
    response_content = json.loads(response.content)

    return response_content["token"]["access"]


@pytest.fixture()
def create_test_teacher(client, create_test_admin):
    data = {
        "email": "teacher@test.com",
        "name": "Teacher",
        "password": "1234",
        "password2": "1234",
    }
    token = create_test_admin
    response = client.post(
        reverse("student:Teacher_Register"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )
    response_content = json.loads(response.content)

    return response_content["token"]["access"]


@pytest.fixture()
def create_test_student(client, create_test_admin):
    data = {
        "email": "student@test.com",
        "name": "Student",
        "roll_no": "roll_no_1",
        "password": "1234",
        "password2": "1234",
    }
    token = create_test_admin
    response = client.post(
        reverse("student:Student_Register"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )
    response_content = json.loads(response.content)

    return response_content["token"]["access"]


@pytest.fixture()
def create_test_course(client, create_test_admin, create_test_teacher):
    data = {
        "name": "Test Course",
        "course_code": "TC123",
        "ch": "4",
    }
    token = create_test_admin

    response = client.post(
        reverse("course:CourseRegisteration"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    return json.loads(response.content)


@pytest.fixture()
def create_test_class(client, create_test_teacher, create_test_course):
    data = {
        "course_code": "TC123",
        "enrollment_start_date": "2022-04-14",
        "enrollment_end_date": "2022-04-18",
        "section": "A",
    }

    token = create_test_teacher
    response = client.post(
        reverse("course:ClassRegister"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    return json.loads(response.content)


@pytest.fixture()
def create_test_timetable(client, create_test_class, create_test_admin):
    token = create_test_admin
    test_class = Classes.objects.first()
    test_class_id = test_class.id

    data = {
        "days": "MONDAY",
        "start_time": "09:30:00",
        "end_time": "10:45:00",
        "_class_": test_class_id,
        "room_no": "ROOM_3",
    }

    response = client.post(
        reverse("course:TimeTableRegisteration"),
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )
    return json.loads(response.content)


"""Fixtures with variables"""


@pytest.fixture()
@patch("accounts.views.admin_views.get_tokens_for_user")
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

        return client.post(reverse("student:Admin_Login"), data)

    return _admin_login


@pytest.fixture()
@patch("accounts.views.teacher_views.get_tokens_for_user")
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

        return client.post(reverse("student:Teacher_Login"), data)

    return _teacher_login


@pytest.fixture()
@patch("accounts.views.student_views.get_tokens_for_user")
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

        return client.post(reverse("student:Student_Login"), data)

    return _student_login


@pytest.fixture()
def create_test_course_with_kwargs(client, create_test_admin, **kwargs):
    def _create_test_course(client, **kwargs):
        token = create_test_admin
        name = kwargs.pop("name")
        course_code = kwargs.pop("course_code")
        ch = kwargs.pop("ch")
        pre_req_courses = kwargs.pop("pre_req_courses")
        data = {
            "name": name,
            "course_code": course_code,
            "ch": ch,
            "pre_req_courses": pre_req_courses,
        }

        return client.post(
            reverse("course:CourseRegisteration"),
            data,
            **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
        )

    return _create_test_course


@pytest.fixture()
def create_test_class_with_kwargs(client, create_test_teacher, **kwargs):
    def _create_test_class(client, **kwargs):
        token = create_test_teacher

        course_code = kwargs.pop("course_code")
        enrollment_start_date = kwargs.pop("enrollment_start_date")
        enrollment_end_date = kwargs.pop("enrollment_end_date")
        section = kwargs.pop("section")
        data = {
            "course_code": course_code,
            "enrollment_start_date": enrollment_start_date,
            "enrollment_end_date": enrollment_end_date,
            "section": section,
        }

        return client.post(
            reverse("course:ClassRegister"),
            data,
            **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
        )

    return _create_test_class


@pytest.fixture()
def create_test_student_with_kwargs(client, create_test_admin, **kwargs):
    def _create_test_student(client, **kwargs):
        token = create_test_admin

        email = kwargs.pop("email")
        name = kwargs.pop("name")
        roll_no = kwargs.pop("roll_no")
        password = kwargs.pop("password")
        password2 = kwargs.pop("password2")
        data = {
            "email": email,
            "name": name,
            "roll_no": roll_no,
            "password": password,
            "password2": password2,
        }

        return client.post(
            reverse("student:Student_Register"),
            data,
            **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
        )

    return _create_test_student
