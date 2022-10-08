from drf_yasg import openapi
from accounts.messages import (
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    PASSWORD_RESET_EMAIL_MESSAGE,
    PASSWORD_RESET_EMAIL_STATUS,
    PASSWORD_RESET_SUCCESS_MESSAGE,
    PASSWORD_RESET_SUCCESS_STATUS,
    USER_WITH_EMAIL_DOESNT_EXIST,
)


send_password_reset_email_response = {
    str(PASSWORD_RESET_EMAIL_STATUS): openapi.Response(
        description="When Reset Password Email Sent Successfully",
        examples={
            "application/json": {
                "msg": PASSWORD_RESET_EMAIL_MESSAGE,
            }
        },
    ),
    "400": openapi.Response(
        description="When User account with the provided email not found",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        USER_WITH_EMAIL_DOESNT_EXIST,
                    ],
                }
            }
        },
    ),
}

password_reset_response = {
    str(PASSWORD_RESET_SUCCESS_STATUS): openapi.Response(
        description="When Password Reset Successfully",
        examples={
            "application/json": {
                "msg": PASSWORD_RESET_SUCCESS_MESSAGE,
            }
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
                }
            }
        },
    ),
    "2: 400": openapi.Response(
        description="When Password Reset Email Expires",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        "Token is not Valid or Expired",
                    ],
                }
            }
        },
    ),
}
