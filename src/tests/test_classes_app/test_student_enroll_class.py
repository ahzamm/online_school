import datetime
import json

import pytest
from classes.models import Course
from django.urls import reverse

pytestmark = pytest.mark.django_db

url = reverse("course:ClassEnrollment", kwargs={"slug": "test-course_a"})


def test_non_student_enroll(client, create_test_teacher, create_test_class):
    """
    Check the response if Non Student User Try to enroll in a Class
    For this Example we uses Teacher as Non Student User
    """
    token = create_test_teacher

    response = client.post(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "errors": {
            "detail": "You do not have permission to perform this action.",
        },
    }


def test_student_already_enrolled(
    client,
    create_test_student,
    create_test_class,
):
    """
    Check the response if the student is already enrolled in the class
    """

    token = create_test_student
    client.post(
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    response = client.post(  # act
        url,
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "data": "You are already enrolled in this course",
    }


def test_pre_req_not_cleared(
    client,
    create_test_student,
    create_test_course_with_kwargs,
    create_test_class_with_kwargs,
):
    """
    Check the response if the student doesn't cleared the pre req course for
    that class
    """
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 1",
        course_code="TC 1",
        ch="4",
        pre_req_courses=[],
    )
    course1 = Course.objects.first()
    create_test_course_with_kwargs(
        client=client,
        name="Test Course 2",
        course_code="TC 2",
        ch="4",
        pre_req_courses=[],
    )
    course2 = Course.objects.get(course_code="TC 2")
    course2.pre_req_courses.add(course1)
    create_test_class_with_kwargs(
        client=client,
        course_code="TC 2",
        enrollment_start_date=datetime.date.today(),
        enrollment_end_date=datetime.date.today(),
        section="A",
    )
    token = create_test_student

    response = client.post(  # act
        reverse("course:ClassEnrollment", kwargs={"slug": "test-course-2_a"}),
        **{"HTTP_AUTHORIZATION": f"Bearer {token}"},
    )

    assert json.loads(response.content) == {
        "data": "You are not eligible for this class yet...",
    }
