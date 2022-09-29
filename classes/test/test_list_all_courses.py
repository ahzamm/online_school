import json

import pytest
from django.urls import reverse

from classes.models import Course

url = reverse("course:ListAllCourse")
pytestmark = pytest.mark.django_db


def test_list_no_courses(client):
    """Check the response when there is no course present in database"""

    response = client.get(url)  # act

    assert (
        response.content.decode("utf-8")
        == '{"count": 0, "next": null, "previous": null, "results": []}'
    )


def test_list_one_courses(client, create_test_course):
    """check if one course is present in our database"""
    # arrange
    course = Course.objects.first()
    response = client.get(url)  # act

    assert response.content.decode("utf-8") == (
        '{"count": 1, "next": null, "previous": null, "results":'
        ' [{"name": "Test Course", "course_detail": '
        '"http://testserver/api/classes/courses/test-course/"}]}'
    )
