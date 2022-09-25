import json
from copy import deepcopy

import pytest
from classes.messages import COURSE_REGISTER_SUCCESS_MESSAGE
from classes.models import Course
from django.urls import reverse

url = reverse("CourseRegisteration")
pytestmark = pytest.mark.django_db

_DATA = {
    "name": "Test Course 1",
    "course_code": "TC123 1",
    "ch": "4",
}


def test_teacher_create_course(client, create_test_teacher):
    """Check the expected response if the for some how teacher
    try to register course
    """
    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert json.loads(response.content) == {
        "errors": {
            "detail": "You do not have permission to perform this action.",
        },
    }


def test_admin_create_course_success(client, create_test_admin):
    """Test of create course success"""
    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    # assert
    assert json.loads(response.content) == {"msg": COURSE_REGISTER_SUCCESS_MESSAGE}


def test_admin_add_heigh_level_course(client, create_test_admin, create_test_course):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin

    response = client.post(  # act
        url,
        data,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    course0 = Course.objects.last()
    course1: Course = Course.objects.first()
    course1.pre_req_courses.add(course0)

    # assert
    assert course0.pre_req.all()[0] == course1
    assert json.loads(response.content) == {
        "msg": COURSE_REGISTER_SUCCESS_MESSAGE,
    }
