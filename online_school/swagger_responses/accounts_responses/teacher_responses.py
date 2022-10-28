from drf_yasg import openapi
from accounts.messages import (
    EMAIL_PASSWORD_NOT_VALID_MESSAGE,
    EMAIL_PASSWORD_NOT_VALID_STATUS,
    LOGIN_SUCCESS_MESSAGE,
    LOGIN_SUCCESS_STATUS,
    PASSWORD_CHANGE_SUCCESS_MESSAGE,
    PASSWORD_CHANGE_SUCCESS_STATUS,
    PASSWORD_CONFIRM_PASSWORD_NOT_MATCH,
    REGISTERATION_SUCCESS_STATUS,
    TEACHER_REGISTERATION_SUCCESS_MESSAGE,
    WRONG_OLD_PASSWORD,
)

REFRESH_TOKEN = "eyJ0eXAiOiJKV..."
ACCESS_TOKEN = "eyJ0eXAiOiJKV..."

teacher_register_response = {
    str(REGISTERATION_SUCCESS_STATUS): openapi.Response(
        description="When Teacher Registeration Successfull",
        examples={
            "application/json": {
                "msg": TEACHER_REGISTERATION_SUCCESS_MESSAGE,
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

teacher_login_response = {
    str(LOGIN_SUCCESS_STATUS): openapi.Response(
        description="When Teacher Loged in Successfully",
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
        description="When Email or Password is not valid",
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

teacher_profile_response = {
    "200": openapi.Response(
        description="When Teacher Visit his/her profile ",
        examples={
            "application/json": {
                "id": "9d814dc2-aa1b-479b-93a9-6f9415721e0b",
                "email": "teacher@test.com",
                "name": "Teacher 1",
            },
        },
    ),
}

teacher_change_password_response = {
    str(PASSWORD_CHANGE_SUCCESS_STATUS): openapi.Response(
        description="When Teacher change his/her account's password",
        examples={
            "application/json": {
                "msg": PASSWORD_CHANGE_SUCCESS_MESSAGE,
            },
        },
    ),
    "1: 400": openapi.Response(
        description="When No account for provided email found",
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
        description="When password and confirm password doesnot match",
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


teacher_detail = {
    "email": "teacher10@test.com",
    "name": "Teacher 10",
    "tea_id": "teacher_no_10",
    "currently_teaching": [
        {
            "course_name": "Test Course 17",
            "section": "C",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-17_c/",
        },
    ],
}

List_one_teacher_response = {
    "200": openapi.Response(
        description="List the detail of one teacher",
        examples={
            "application/json": teacher_detail,
        },
    ),
}


teacher_list = {
    "count": 32,
    "next": "http://localhost:8000/api/account/teachers/?page=2",
    "previous": "null",
    "results": [
        {
            "tea_id": "teacher_no_0",
            "teacher_detail": "http://localhost:8000/api/account/teachers/teacher_no_0/",
        },
        {
            "tea_id": "teacher_no_1",
            "teacher_detail": "http://localhost:8000/api/account/teachers/teacher_no_1/",
        },
    ],
}

list_all_teacher_response = {
    "200": openapi.Response(
        description="List all the teacher",
        examples={
            "application/json": teacher_list,
        },
    ),
}
