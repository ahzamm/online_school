from rest_framework.pagination import PageNumberPagination


class ListAllCoursePagination(PageNumberPagination):
    page_size = 5
