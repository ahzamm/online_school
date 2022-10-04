import pytest
import json
from django.urls import reverse

from classes.models import Course

url = reverse("course:CourseDetail", kwargs={"slug": "test-course-999"})
pytestmark = pytest.mark.django_db


def test_no_course_detail(client):
    """
    Check the response if no course is present in our database / wrong slug
    """
    response = client.get(url)  # act

    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_lvl_1_course_detail(client, create_test_course_with_kwargs):
    """Check the response if there is one level 1 coure present in our DB"""

    create_test_course_with_kwargs(
        client=client,
        name="Test Course 1",
        course_code="TC 1",
        ch="4",
        pre_req_courses=[],
    )

    response = client.get(
        reverse(
            "course:CourseDetail",
            kwargs={"slug": "test-course-1"},
        ),
    )  # act

    assert json.loads(response.content) == [
        {
            "name": "Test Course 1",
            "course_code": "TC 1",
            "ch": 4,
            "pre_req_courses": [],
        },
    ]


@pytest.mark.xfail(
    reason="It may failed because of random sorting of dictionary",
)
def test_lvl_x_course_detail(client, create_test_course_with_kwargs):
    """
    Check the response if there is x level 1 coure present in our DB
    where x is greater than 1
    """

    create_test_course_with_kwargs(
        client=client,
        name="Test Course 1",
        course_code="TC 1",
        ch="4",
        pre_req_courses=[],
    )
    pre_req_courses_ids = [Course.objects.get(name="Test Course 1").id]
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 2",
        course_code="TC 2",
        ch="4",
        pre_req_courses=[],
    )
    pre_req_courses_ids.append(Course.objects.get(name="Test Course 2").id)
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 3",
        course_code="TC 3",
        ch="4",
        pre_req_courses=[],
    )
    pre_req_courses_ids.append(Course.objects.get(name="Test Course 3").id)
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 4",
        course_code="TC 4",
        ch="4",
        pre_req_courses=pre_req_courses_ids,
    )

    response = client.get(  # act
        reverse(
            "course:CourseDetail",
            kwargs={"slug": "test-course-4"},
        ),
    )

    predicted_response = [
        {
            "name": "Test Course 4",
            "course_code": "TC 4",
            "ch": 4,
            "pre_req_courses": [
                {
                    "name": "Test Course 2",
                    "course_detail": "http://testserver/api/classes/courses/test-course-2/",
                },
                {
                    "name": "Test Course 1",
                    "course_detail": "http://testserver/api/classes/courses/test-course-1/",
                },
                {
                    "name": "Test Course 3",
                    "course_detail": "http://testserver/api/classes/courses/test-course-3/",
                },
            ],
        },
    ]
    assert json.loads(response.content) == predicted_response
