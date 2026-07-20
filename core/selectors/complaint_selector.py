
from django.shortcuts import get_object_or_404

from core.models import Complaint


class ComplaintSelector:
    """
    Read-only queries for complaint details.
    """

    @staticmethod
    def get_complaint(complaint_id):
        return (
            Complaint.objects
            .with_related()
            .prefetch_related(
                "images",
                "status_logs",
            )
            .get(
                complaint_id=complaint_id,
            )
        )

    @staticmethod
    def get_complaint_or_404(complaint_id):
        return get_object_or_404(
            Complaint.objects.with_related(),
            complaint_id=complaint_id,
        )

    @staticmethod
    def list_status_logs(complaint):
        return complaint.status_logs.order_by(
            "timestamp",
        )