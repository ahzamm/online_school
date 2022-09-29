from rest_framework.pagination import PageNumberPagination


class ListAllCoursesPagination(PageNumberPagination):
    page_size = 10
