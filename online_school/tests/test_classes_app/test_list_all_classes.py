import pytest
from django.urls import reverse

url = reverse("course:ListAllClasses")
pytestmark = pytest.mark.django_db


def test_list_no_classes(client, create_test_student):
    """Check the response when there is no class present in database"""
    token = create_test_student

    response = client.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})  # act

    assert (
        response.content.decode("utf-8")
        == '{"count": 0, "next": null, "previous": null, "results": []}'
    )


def test_list_one_classes(client, create_test_class, create_test_student):
    """check if one course is present in our database"""
    token = create_test_student

    response = client.get(url, **{"HTTP_AUTHORIZATION": f"Bearer {token}"})  # act

    assert response.content.decode("utf-8") == (
        '{"count": 1, "next": null, "previous": null, "results":'
        ' [{"course_name": "Test Course", "section": "A", "class_detail": '
        '"http://testserver/api/classes/classes/test-course_a/"}]}'
    )
