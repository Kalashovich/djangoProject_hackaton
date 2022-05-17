from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'
    max_page_size = 1000
    invalid_page_message = (
        'Такой страницы не существует!'
    )

