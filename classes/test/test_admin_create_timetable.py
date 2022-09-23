import json
from copy import deepcopy

import pytest
from classes.messages import (INVALID_TIME_MESSAGE,
                              TIMETABLE_REGISTER_SUCCESS_MESSAGE,
                              no_class_found, timetable_clash_message)
from classes.models import Classes
from django.urls import reverse

from .extra import non_field_error

url = reverse('TimeTableRegisteration')
pytestmark = pytest.mark.django_db


_DATA = {"days": "MONDAY",
         "start_time": "09:30:00",
         "end_time": "10:45:00",
         "_class_": "b1299dbc3259437fa9775901807412a7",
         "room_no": "ROOM_3"}


def test_invalid_course(client, create_test_class, create_test_admin):

    # arrange
    token = create_test_admin
    data = deepcopy(_DATA)

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    response_content = json.loads(response.content)
    response_content["errors"]["non_field_errors"][0] = \
        response_content["errors"]["non_field_errors"][0].replace('-', '')

    # assert
    assert response_content == non_field_error(
        no_class_found(data["_class_"]))


def test_time_clash(client, create_test_class, create_test_admin,
                    create_test_timetable):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    test_class = Classes.objects.first()
    test_class_id = test_class.id
    data["_class_"] = test_class_id
    data["start_time"] = "10:30:00"
    data["end_time"] = "11:40:00"

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    # assert
    assert json.loads(response.content) == non_field_error(
        timetable_clash_message(
            data[
                "room_no"
            ],
        ),
    )


def test_invalid_time(client, create_test_class, create_test_admin,
                      create_test_timetable):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    test_class = Classes.objects.first()
    test_class_id = test_class.id
    data["_class_"] = test_class_id
    data["start_time"] = "10:30:00"
    data["end_time"] = "09:40:00"

    response = client.post(  # act
        url,
        data,
        **{'HTTP_AUTHORIZATION': f'Bearer {token}'},
    )

    # assert
    assert json.loads(response.content) == non_field_error(
        INVALID_TIME_MESSAGE)


def test_create_timetable(client, create_test_class, create_test_admin):

    # arrange
    data = deepcopy(_DATA)
    token = create_test_admin
    test_class = Classes.objects.first()
    test_class_id = test_class.id
    data["_class_"] = test_class_id

    response = client.post(  # act
        url, data, **{'HTTP_AUTHORIZATION': f'Bearer {token}'})

    # assert
    assert json.loads(response.content) == {
        'msg': TIMETABLE_REGISTER_SUCCESS_MESSAGE}
