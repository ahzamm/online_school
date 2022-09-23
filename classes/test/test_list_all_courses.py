import json
from copy import deepcopy

import pytest
from django.urls import reverse
from classes.helper import UUIDEncoder
from .extra import non_field_error

url = reverse('ListAllCourse')
pytestmark = pytest.mark.django_db


def test_list_no_courses(client):
    """Check the response when there is no course present in database"""

    response = client.get(url) # act

    assert response.content.decode('utf-8') == '{"data": []}'
