DUMMY_TOKEN = {
    "refresh": "DummyRefreshToken",
    "access": "DummyAccessToken",
}


def non_field_error(message):
    return {"errors": {"non_field_errors": [message]}}
