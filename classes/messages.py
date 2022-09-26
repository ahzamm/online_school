COURSE_REGISTER_SUCCESS_MESSAGE = "COURSE ADDED SUCCESSFULLY"
COURSE_REGISTER_SUCCESS_STATUS = 201

NO_TEACHER_FOUND_MESSAGE = "No Teacher with this Email found"


TIMETABLE_REGISTER_SUCCESS_MESSAGE = "TIMETABLE ADDED SUCCESSFULLY"
TIMETABLE_REGISTER_SUCCESS_STATUS = 201


def timetable_clash_message(room_no: str) -> str:
    return f"There is already a class on this time in room no {room_no}"


INVALID_TIME_MESSAGE = "The provided time is invalid"


def no_class_found(id: int):
    return f"No class with ID {id} found"


CLASS_CREATE_SUCCESS_MESSAGE = "Class Added Successfully"
CLASS_CREATE_SUCCESS_STATUS = 200

CLASS_ALREADY_REGISTERED = "Class with this course and section already exists"

NO_COURSE_ERROR_MESSAGE = "No course with this course code present"

ALREADY_ENROLLED_MESSAGE = "You are already enrolled in this course"
