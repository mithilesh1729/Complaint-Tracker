from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsHostelOffice

from core.filters import ComplaintFilter
from core.selectors.complaint_list_selector import ComplaintListSelector
from core.serializers.complaint_list_serializers import ComplaintListSerializer

class OfficeQueueAPIView(ListAPIView):
    """
    Complaints waiting for assignment.
    """

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    serializer_class = ComplaintListSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ComplaintFilter

    search_fields = [
        "complaint_number",
        "user__name",
        "category__name",
    ]

    ordering_fields = [
        "created_at",
        "priority",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return ComplaintListSelector.get_office_queue()