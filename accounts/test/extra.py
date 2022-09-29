DUMMY_TOKEN = {
    "refresh": "DummyRefreshToken",
    "access": "DummyAccessToken",
}

FIELD_REQUIRED_MESSAGE = {
    "errors": {
        "email": [
            "This field is required.",
        ],
        "name": [
            "This field is required.",
        ],
        "password": [
            "This field is required.",
        ],
        "password2": [
            "This field is required.",
        ],
    },
}


STUDENT_FIELD_REQUIRED_MESSAGE = {
    "errors": {
        "email": [
            "This field is required.",
        ],
        "name": [
            "This field is required.",
        ],
        "roll_no": [
            "This field is required.",
        ],
        "password": [
            "This field is required.",
        ],
        "password2": [
            "This field is required.",
        ],
    },
}


def non_field_error(message):
    return {"errors": {"non_field_errors": [message]}}
