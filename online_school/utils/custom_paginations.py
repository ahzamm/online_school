from rest_framework.pagination import PageNumberPagination


class ListAllCoursesPagination(PageNumberPagination):
    page_size = 10


class ListAllStudentPagination(PageNumberPagination):
    page_size = 10


class ListAllTeacherPagination(PageNumberPagination):
    page_size = 10
