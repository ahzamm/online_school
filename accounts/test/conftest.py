import json
import pytest
from django.urls import reverse

url = reverse("Admin_Register")


@pytest.fixture
def create_test_admin(client):
    data = {
        "email": "admin@test.com",
        "name": "Admin",
        "password": "1234",
        "password2": "1234"
    }
    response = client.post(url, data)
    response_content = json.loads(response.content)
    return response_content['token']['access']
