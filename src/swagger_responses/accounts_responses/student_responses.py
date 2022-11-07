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
    STUDENT_REGISTERATION_SUCCESS_MESSAGE,
    WRONG_OLD_PASSWORD,
)

REFRESH_TOKEN = "eyJ0eXAiOiJKV..."
ACCESS_TOKEN = "eyJ0eXAiOiJKV..."

student_register_response = {
    str(REGISTERATION_SUCCESS_STATUS): openapi.Response(
        description="When Student Registeration Successfull",
        examples={
            "application/json": {
                "msg": STUDENT_REGISTERATION_SUCCESS_MESSAGE,
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

student_login_response = {
    str(LOGIN_SUCCESS_STATUS): openapi.Response(
        description="When Student Loged in Successfully",
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

student_profile_response = {
    "200": openapi.Response(
        description="When Student Visit his/her profile ",
        examples={
            "application/json": {
                "id": "9d814dc2-aa1b-479b-93a9-6f9415721e0b",
                "email": "student@test.com",
                "name": "Student 1",
            },
        },
    ),
}

student_change_ts_password_response = {
    str(PASSWORD_CHANGE_SUCCESS_STATUS): openapi.Response(
        description="When Student change his/her account's password",
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

student_detail = {
    "email": "student86@test.com",
    "name": "Student 86",
    "roll_no": "roll_no_86",
    "grade": "Five",
    "cleared_course": [
        {
            "name": "Test Course 16",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-16/",
        },
        {
            "name": "Test Course 35",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-35/",
        },
    ],
}

List_one_student_response = {
    "200": openapi.Response(
        description="List the detail of one student",
        examples={
            "application/json": student_detail,
        },
    ),
}

student_list = {
    "count": 997,
    "next": "http://localhost:8000/api/account/students/?page=10",
    "previous": "http://localhost:8000/api/account/students/?page=8",
    "results": [
        {
            "roll_no": "roll_no_80",
            "student_detail": "http://localhost:8000/api/account/students/roll_no_80/",
        },
        {
            "roll_no": "roll_no_81",
            "student_detail": "http://localhost:8000/api/account/students/roll_no_81/",
        },
        {
            "roll_no": "roll_no_82",
            "student_detail": "http://localhost:8000/api/account/students/roll_no_82/",
        },
    ],
}

List_all_student_response = {
    "200": openapi.Response(
        description="List All Students",
        examples={
            "application/json": student_list,
        },
    ),
}
