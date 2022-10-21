from accounts.views import AdminDeleteCourse
from django.urls import path

from .views import (
    AdminCreateCourseView,
    AdminCreateTimeTableView,
    ListAllClassesView,
    ListAllCoursesView,
    ListOneClassView,
    ListOneCourseView,
    StudentEnrollClassView,
    TeacherCreateClassView,
)

urlpatterns = [
    path(
        "course-register/",
        AdminCreateCourseView.as_view(),
        name="CourseRegisteration",
    ),
    path(
        "timetable-register/",
        AdminCreateTimeTableView.as_view(),
        name="TimeTableRegisteration",
    ),
    path(
        "class-register/",
        TeacherCreateClassView.as_view(),
        name="ClassRegister",
    ),
    path(
        "courses/",
        ListAllCoursesView.as_view(),
        name="ListAllCourse",
    ),
    path(
        "courses/<slug>/",
        ListOneCourseView.as_view(),
        name="CourseDetail",
    ),
    path(
        "courses/<slug>/delete/",
        AdminDeleteCourse.as_view(),
        name="CourseDelete",
    ),
    path(
        "classes/",
        ListAllClassesView.as_view(),
        name="ListAllClasses",
    ),
    path(
        "classes/<slug>/",
        ListOneClassView.as_view(),
        name="ClassDetail",
    ),
    path(
        "classes/<slug>/enroll/",
        StudentEnrollClassView.as_view(),
        name="ClassEnrollment",
    ),
]
