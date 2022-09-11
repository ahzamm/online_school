from django.urls import path

from .views import *

urlpatterns = [
    path('course-register/', AdminCreateCourse.as_view(),
         name="CourseRegisteration")
]
