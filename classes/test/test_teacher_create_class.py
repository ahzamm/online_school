import json
from copy import deepcopy

import pytest
from django.urls import reverse

from classes.messages import (
    CLASS_ALREADY_REGISTERED,
    CLASS_CREATE_SUCCESS_MESSAGE,
    NO_COURSE_ERROR_MESSAGE,
)

from .extra import non_field_error

url = reverse("ClassRegister")
pytestmark = pytest.mark.django_db

_DATA = {
    "course_code": "TC123",
    "enrollment_start_date": "2022-04-14",
    "enrollment_end_date": "2022-04-18",
    "section": "A",
}


def test_admin_create_class(client, create_test_admin, create_test_class):
    """Check the expected response if admin try to create class"""
    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin

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


def test_create_class_with_wrong_coursecode(client, create_test_teacher):
    """Test the response by providing the course code, having no entry in our
    database
    """
    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(  # act
        url, data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"}
    )

    # assert
    assert json.loads(response.content) == non_field_error(
        NO_COURSE_ERROR_MESSAGE
    )


def test_already_registered_class(
    client, create_test_teacher, create_test_course, create_test_class
):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(
        url, data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"}  # act
    )

    # assert
    assert json.loads(response.content) == non_field_error(
        CLASS_ALREADY_REGISTERED
    )


def test_create_class_success(client, create_test_teacher, create_test_course):
    """Test the response by providing all valid data of in order to register a
    class
    """
    # arrange
    data = deepcopy(_DATA)
    token = create_test_teacher

    response = client.post(  # act
        url, data, **{"HTTP_AUTHORIZATION": f"Bearer {token}"}
    )

    # assert
    assert json.loads(response.content) == {
        "msg": CLASS_CREATE_SUCCESS_MESSAGE
    }
