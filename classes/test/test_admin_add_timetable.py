import pytest
from django.urls import reverse
import json
from classes.messages import *

url = reverse('TimeTableRegisteration')
pytestmark = pytest.mark.django_db


DATA = {"days": "MONDAY",
        "start_time": "09:30:00",
        "end_time": "10:45:00",
        "_class_": "b1299dbc3259437fa9775901807412a7",
        "room_no": "ROOM_3"}


def test_create_timetable(client, create_test_course, create_test_admin):
    teacher_id = ...
    token = create_test_admin
