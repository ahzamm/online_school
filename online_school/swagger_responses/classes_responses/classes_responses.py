from drf_yasg import openapi
from classes.messages import (
    ALREADY_ENROLLED_MESSAGE,
    CLASS_ALREADY_REGISTERED,
    CLASS_CREATE_SUCCESS_MESSAGE,
    CLASS_CREATE_SUCCESS_STATUS,
    COURSE_REGISTER_SUCCESS_MESSAGE,
    COURSE_REGISTER_SUCCESS_STATUS,
    ENROLLED_SUCCESS_MESSAGE,
    INVALID_TIME_MESSAGE,
    NO_COURSE_ERROR_MESSAGE,
    NOT_ELIGIBLE_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_MESSAGE,
    TIMETABLE_REGISTER_SUCCESS_STATUS,
    timetable_clash_message,
)

course_register_response = {
    str(COURSE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Registeration Successfull",
        examples={
            "application/json": {
                "msg": COURSE_REGISTER_SUCCESS_MESSAGE,
            },
        },
    ),
}


class_register_response = {
    str(CLASS_CREATE_SUCCESS_STATUS): openapi.Response(
        description="When Teacher Successfully Registeration Class",
        examples={
            "application/json": {
                "msg": CLASS_CREATE_SUCCESS_MESSAGE,
            },
        },
    ),
    "1: 400": openapi.Response(
        description="When the Course Not Found",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        NO_COURSE_ERROR_MESSAGE,
                    ],
                },
            },
        },
    ),
    "2: 400": openapi.Response(
        description="When Class with same Course and Sectionalready Registered",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        CLASS_ALREADY_REGISTERED,
                    ],
                },
            },
        },
    ),
}


timetable_register_response = {
    str(TIMETABLE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Successfully Registeration Class",
        examples={
            "application/json": {
                "msg": TIMETABLE_REGISTER_SUCCESS_MESSAGE,
            },
        },
    ),
    "1: 400": openapi.Response(
        description="When class End time is less than starting time",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        INVALID_TIME_MESSAGE,
                    ],
                },
            },
        },
    ),
    "2: 400": openapi.Response(
        description="When there is already a class going on in provided ROOM NO at that time",
        examples={
            "application/json": {
                "errors": {
                    "non_field_errors": [
                        timetable_clash_message("104"),
                    ],
                },
            },
        },
    ),
}


all_courses = {
    "count": 89,
    "next": "http://localhost:8000/api/classes/courses/?page=8",
    "previous": "http://localhost:8000/api/classes/courses/?page=6",
    "results": [
        {
            "name": "Test Course 61",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-61/",
        },
        {
            "name": "Test Course 62",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-62/",
        },
        {
            "name": "Test Course 63",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-63/",
        },
    ],
}


list_all_course_response = {
    str(TIMETABLE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Successfully Registeration Class",
        examples={
            "application/json": all_courses,
        },
    ),
}


course_detail = [
    {
        "name": "Test Course 78",
        "course_code": "TC 78",
        "ch": 4,
        "pre_req_courses": [
            {
                "name": "Test Course 52",
                "course_detail": "http://localhost:8000/api/classes/courses/test-course-52/",
            },
            {
                "name": "Test Course 42",
                "course_detail": "http://localhost:8000/api/classes/courses/test-course-42/",
            },
            {
                "name": "Test Course 54",
                "course_detail": "http://localhost:8000/api/classes/courses/test-course-54/",
            },
        ],
    }
]


list_one_course_response = {
    str(TIMETABLE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Successfully Registeration Class",
        examples={
            "application/json": course_detail,
        },
    ),
}


all_classes = {
    "count": 80,
    "next": "http://localhost:8000/api/classes/classes/?page=6",
    "previous": "http://localhost:8000/api/classes/classes/?page=4",
    "results": [
        {
            "course_name": "Test Course 66",
            "section": "A",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-66_a/",
        },
        {
            "course_name": "Test Course 77",
            "section": "C",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-77_c/",
        },
        {
            "course_name": "Test Course 67",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-67_b/",
        },
        {
            "course_name": "Test Course 74",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-74_b/",
        },
        {
            "course_name": "Test Course 66",
            "section": "A",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-66_a/",
        },
        {
            "course_name": "Test Course 67",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-67_b/",
        },
        {
            "course_name": "Test Course 73",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-73_b/",
        },
        {
            "course_name": "Test Course 77",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-77_b/",
        },
        {
            "course_name": "Test Course 73",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-73_b/",
        },
        {
            "course_name": "Test Course 70",
            "section": "B",
            "class_detail": "http://localhost:8000/api/classes/classes/test-course-70_b/",
        },
    ],
}


list_all_class_response = {
    str(TIMETABLE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Successfully Registeration Class",
        examples={
            "application/json": all_classes,
        },
    ),
}


class_detail = [
    {
        "course": {
            "name": "Test Course 70",
            "course_detail": "http://localhost:8000/api/classes/courses/test-course-70/",
        },
        "teacher_name": "Teacher 4",
        "enrollment_start_date": "2022-10-04",
        "enrollment_end_date": "2022-10-04",
        "section": "B",
        "mid_exammination_date": "2022-10-04",
        "final_exammination_date": "2022-10-04",
        "student": [
            {
                "roll_no": "roll_no_711",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_711/",
            },
            {
                "roll_no": "roll_no_673",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_673/",
            },
            {
                "roll_no": "roll_no_672",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_672/",
            },
            {
                "roll_no": "roll_no_718",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_718/",
            },
            {
                "roll_no": "roll_no_765",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_765/",
            },
            {
                "roll_no": "roll_no_749",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_749/",
            },
            {
                "roll_no": "roll_no_636",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_636/",
            },
            {
                "roll_no": "roll_no_787",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_787/",
            },
            {
                "roll_no": "roll_no_680",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_680/",
            },
            {
                "roll_no": "roll_no_770",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_770/",
            },
            {
                "roll_no": "roll_no_681",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_681/",
            },
            {
                "roll_no": "roll_no_699",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_699/",
            },
            {
                "roll_no": "roll_no_740",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_740/",
            },
            {
                "roll_no": "roll_no_792",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_792/",
            },
            {
                "roll_no": "roll_no_643",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_643/",
            },
            {
                "roll_no": "roll_no_647",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_647/",
            },
            {
                "roll_no": "roll_no_612",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_612/",
            },
            {
                "roll_no": "roll_no_641",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_641/",
            },
            {
                "roll_no": "roll_no_726",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_726/",
            },
            {
                "roll_no": "roll_no_697",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_697/",
            },
            {
                "roll_no": "roll_no_635",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_635/",
            },
            {
                "roll_no": "roll_no_646",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_646/",
            },
            {
                "roll_no": "roll_no_744",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_744/",
            },
            {
                "roll_no": "roll_no_665",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_665/",
            },
            {
                "roll_no": "roll_no_769",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_769/",
            },
            {
                "roll_no": "roll_no_767",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_767/",
            },
            {
                "roll_no": "roll_no_793",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_793/",
            },
            {
                "roll_no": "roll_no_638",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_638/",
            },
            {
                "roll_no": "roll_no_625",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_625/",
            },
            {
                "roll_no": "roll_no_678",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_678/",
            },
            {
                "roll_no": "roll_no_778",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_778/",
            },
            {
                "roll_no": "roll_no_632",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_632/",
            },
            {
                "roll_no": "roll_no_634",
                "student_detail": "http://localhost:8000/api/account/students/roll_no_634/",
            },
        ],
    },
]


list_one_class_response = {
    str(TIMETABLE_REGISTER_SUCCESS_STATUS): openapi.Response(
        description="When Admin Successfully Registeration Class",
        examples={
            "application/json": class_detail,
        },
    ),
}


class_enrollment = {
    "200": openapi.Response(
        description="When Student successfully enroll in a class",
        examples={
            "application/json": {"data": ENROLLED_SUCCESS_MESSAGE},
        },
    ),
    "1: 400": openapi.Response(
        description=(
            "When Student didnot cleared the Pre Requsite Courses Required for that class"
        ),
        examples={
            "application/json": {"data": NOT_ELIGIBLE_MESSAGE},
        },
    ),
    "2: 400": openapi.Response(
        description="When Student is already enrolled in the class",
        examples={
            "application/json": {"data": ALREADY_ENROLLED_MESSAGE},
        },
    ),
}
