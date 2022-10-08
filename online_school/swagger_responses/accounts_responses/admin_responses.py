from accounts.messages import (
    ADMIN_REGISTERATION_SUCCESS_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    REGISTERATION_SUCCESS_STATUS,
)
from drf_yasg import openapi


REFRESH_TOKEN = "eyJ0eXAiOiJKV..."
ACCESS_TOKEN = "eyJ0eXAiOiJKV..."


admin_register_response = {
    str(REGISTERATION_SUCCESS_STATUS): openapi.Response(
        description="Admin Registeration Successfull",
        examples={
            "application/json": {
                "msg": ADMIN_REGISTERATION_SUCCESS_MESSAGE,
            }
        },
    ),
    "400": openapi.Response(
        description="When Password and Confirm Password Doesn't Match",
        examples={
            "application/json": {
                "error": PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
            }
        },
    ),
}

admin_login_response = {
    str(LOGIN_SUCCESS_STATUS): openapi.Response(
        description="When Login Successfully",
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
        description="When Password and Confirm Password Doesn't Match",
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
        description="Admin Registeration Successfull",
        examples={
            "application/json": {
                "id": "9d814dc2-aa1b-479b-93a9-6f9415721e0b",
                "email": "admin1@test.com",
                "name": "Admin 1",
            }
        },
    ),
}
