from django.db.models import Count, Q
from django.utils import timezone

from core.models import Complaint


class OfficeDashboardSelector:
    """
    Read-only queries for Hostel Office dashboard.
    """

    @classmethod
    def get_dashboard(cls, user):
        return {
            "stats": cls._get_stats(user),
            "recent_complaints": cls._get_recent_complaints(),
        }

    @classmethod
    def _get_stats(cls, user):
        today = timezone.localdate()

        stats = Complaint.objects.aggregate(
            pending=Count(
                "id",
                filter=Q(
                    status="pending",
                ),
            ),

            resolved_today=Count(
                "id",
                filter=Q(
                    status="resolved",
                    resolved_at__date=today,
                ),
            ),

            high_priority=Count(
                "id",
                filter=Q(
                    priority="high",
                )
                & Q(
                    status__in=[
                        "pending",
                        "in_progress",
                    ],
                ),
            ),
        )

        stats["assigned"] = (
            Complaint.objects
            .assigned_to(user)
            .in_progress()
            .count()
        )

        return stats

    @classmethod
    def _get_recent_complaints(cls):
        return (
            Complaint.objects
            .with_related()
            .latest()[:5]
        )