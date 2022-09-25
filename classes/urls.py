from django.urls import path

from .views import (
    AdminCreateCourseView,
    AdminCreateTimeTableView,
    ListAllClassesView,
    ListAllCoursesView,
    ListOneCourseView,
    TeacherCreateClassView,
    ListOneClassView,
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
        "classes/",
        ListAllClassesView.as_view(),
        name="ListAllClasses",
    ),
    path(
        "classes/<slug>/",
        ListOneClassView.as_view(),
        name="ClassDetail",
    ),
]
