from rest_framework.pagination import PageNumberPagination

class GlobalPagination(PageNumberPagination):
    """
    Unified pagination class for the entire application.
    Enforces a strict max_page_size to prevent DoS attacks via huge database queries.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 50
