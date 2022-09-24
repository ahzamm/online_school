from django.urls import path

from .views import (AdminCreateCourse, AdminCreateTimeTable,
                    ListAllCoursesView, ListOneCourse, TeacherCreateClassView)

urlpatterns = [
    path('course-register/', AdminCreateCourse.as_view(),
         name="CourseRegisteration"),
    path('timetable-register/', AdminCreateTimeTable.as_view(),
         name="TimeTableRegisteration"),
    path('class-register/', TeacherCreateClassView.as_view(),
         name='ClassRegister'),
    path('courses/', ListAllCoursesView.as_view(),
         name='ListAllCourse'),
    path('courses/<slug>/', ListOneCourse.as_view(), name='CourseDetail'),

]
