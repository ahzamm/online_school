import json

import pytest
from classes.models import Course
from django.urls import reverse

url = reverse('ListAllCourse')
pytestmark = pytest.mark.django_db


def test_list_no_courses(client):
    """Check the response when there is no course present in database"""

    response = client.get(url)  # act

    assert response.content.decode('utf-8') == '{"data": []}'


def test_list_one_courses(client, create_test_course):
    """check if one course is present in our database"""
    # arrange
    course = Course.objects.first()
    message = {
        "data": [{
            "id": str(course.id),
            "name": str(course.name),
            "course_code": str(course.course_code),
            "ch": course.ch,
            "pre_req_courses": [],
            },
        ],
    }

    response = client.get(url)  # act

    assert response.content.decode('utf-8') == json.dumps(message)
