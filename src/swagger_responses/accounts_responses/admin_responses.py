from accounts.messages import (
    ADMIN_REGISTERATION_SUCCESS_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CHANGE_SUCCESS_MESSAGE,
    PASSWORD_CHANGE_SUCCESS_STATUS,
    REGISTERATION_SUCCESS_STATUS,
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    NO_STUDENT_TEACHER_WITH_EMAIL,
    WRONG_OLD_PASSWORD,
)
from drf_yasg import openapi


REFRESH_TOKEN = "eyJ0eXAiOiJKV..."
ACCESS_TOKEN = "eyJ0eXAiOiJKV..."


admin_register_response = {
    str(REGISTERATION_SUCCESS_STATUS): openapi.Response(
        description="When Admin Registeration Successfull",
        examples={
            "application/json": {
                "msg": ADMIN_REGISTERATION_SUCCESS_MESSAGE,
            },
        },
    ),
    "400": openapi.Response(
        description="When Password and Confirm Password Doesn't Match",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
                    ],
                },
            },
        },
    ),
}

admin_login_response = {
    str(LOGIN_SUCCESS_STATUS): openapi.Response(
        description="When Admin Loged in Successfully",
        examples={
            "application/json": {
                "msg": LOGIN_SUCCESS_MESSAGE,
                "token": {
                    "refresh": REFRESH_TOKEN,
                    "access": ACCESS_TOKEN,
                },
            },
        },
    ),
    str(EMAIL_PASSWORD_NOT_VALID_STATUS): openapi.Response(
        description="When Email and Password is not valid",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        EMAIL_PASSWORD_NOT_VALID_MESSAGE,
                    ],
                },
            },
        },
    ),
}

admin_profile_response = {
    str(REGISTERATION_SUCCESS_STATUS): openapi.Response(
        description="When Admin Visit his/her profile ",
        examples={
            "application/json": {
                "id": "9d814dc2-aa1b-479b-93a9-6f9415721e0b",
                "email": "admin1@test.com",
                "name": "Admin 1",
            },
        },
    ),
}

admin_change_ts_password_response = {
    str(PASSWORD_CHANGE_SUCCESS_STATUS): openapi.Response(
        description="Admin Change password of a Teacher or Student account",
        examples={
            "application/json": {
                "msg": PASSWORD_CHANGE_SUCCESS_MESSAGE,
            },
        },
    ),
    "400": openapi.Response(
        description="When No account for provided email found",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        NO_STUDENT_TEACHER_WITH_EMAIL,
                    ],
                },
            },
        },
    ),
}


admin_change_password_response = {
    str(PASSWORD_CHANGE_SUCCESS_STATUS): openapi.Response(
        description="Admin Change password of his own account",
        examples={
            "application/json": {
                "msg": PASSWORD_CHANGE_SUCCESS_MESSAGE,
            },
        },
    ),
    "1: 400": openapi.Response(
        description="When Password and Confirm Password Doesn't Match",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
                    ],
                },
            },
        },
    ),
    "2: 400": openapi.Response(
        description="When Wrong old password provided",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        WRONG_OLD_PASSWORD,
                    ],
                },
            },
        },
    ),
}
