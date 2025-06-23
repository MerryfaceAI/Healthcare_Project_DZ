from rest_framework.pagination import PageNumberPagination

class PatientPagination(PageNumberPagination):
    """
    Shared pagination settings for all Patient-related APIs.
    """
    page_size = 10
    page_size_query_param = 'page_size'