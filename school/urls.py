from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/account/", include("accounts.urls")),
    path(
        "api/classes/", include(("classes.urls", "Course"), namespace="course")
    ),
]
