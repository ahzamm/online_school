import json
from classes.models import Course
from copy import deepcopy

import pytest
from classes.messages import *
from django.urls import reverse

url = reverse('CourseRegisteration')
pytestmark = pytest.mark.django_db

_DATA = {"name": "Test Course 1", "course_code": "TC123 1",
         "ch": "4"}


def test_teacher_create_course(client, create_test_teacher):
    """Check the expected response if the for some how teacher
       try to register course
    """

    DATA = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    error_message = {'errors': {
        'detail': 'You do not have permission to perform this action.'}}
    assert response_content == error_message


def test_admin_create_course_success(client, create_test_admin):
    """Test of create course success
    """

    DATA = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    success_message = {'msg': COURSE_REGISTER_SUCCESS_MESSAGE}
    assert response_content == success_message


def test_admin_add_heigh_level_course(client, create_test_admin, create_test_course):
    DATA = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(
        url, DATA, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)

    course0 = Course.objects.last()
    course1: Course = Course.objects.first()
    course1.pre_req_courses.add(course0)

    success_message = {'msg': COURSE_REGISTER_SUCCESS_MESSAGE}

    assert course0.pre_req.all()[0] == course1
    assert response_content == success_message
