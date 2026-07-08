from django.db.models import Count

from core.models import Complaint
from django.db import models

class DashboardSelector:

    @staticmethod
    def get_student_dashboard_data(user):

        complaints = Complaint.objects.filter(
            user=user
        )

        stats = complaints.aggregate(
            total=Count("id"),
            pending=Count(
                "id",
                filter=models.Q(status="pending"),
            ),
            in_progress=Count(
                "id",
                filter=models.Q(status="in_progress"),
            ),
            resolved=Count(
                "id",
                filter=models.Q(status="resolved"),
            ),
        )

        stats["active"] = (
            stats["pending"] +
            stats["in_progress"]
        )

        recent = (
            complaints
            .select_related("category")
            .order_by("-created_at")[:5]
        )

        return {
            "stats": stats,
            "recent": recent,
        }