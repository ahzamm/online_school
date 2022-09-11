import pytest
from django.urls import reverse
import json

url = reverse('CourseRegisteration')
pytestmark = pytest.mark.django_db


def test_admin_create_course(client, create_test_admin, create_test_teacher):
    token = create_test_admin
    data = {"name": "Test Course", "course_code": "TC123",
            "ch": "4", "email": "teacher@test.com"}
    response = client.post(
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})
    response_content = json.loads(response.content)
    success_message = {'msg': 'COURSE ADDED SUCCESSFULLY'}
    assert response_content == success_message
