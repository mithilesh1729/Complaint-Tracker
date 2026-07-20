from django.db.models import Count, Q
from core.models import Complaint, User, ComplaintCategory

class AdminDashboardSelector:
    """
    Read-only queries for Admin dashboard.
    """

    @classmethod
    def get_dashboard(cls):
        return {
            "stats": cls._get_stats(),
        }

    @classmethod
    def _get_stats(cls):
        complaint_stats = Complaint.objects.aggregate(
            total_complaints=Count("pk"),
            pending=Count("pk", filter=Q(status="pending")),
            in_progress=Count("pk", filter=Q(status="in_progress")),
            resolved=Count("pk", filter=Q(status="resolved")),
            high_priority=Count("pk", filter=Q(priority="high")),
        )

        user_stats = User.objects.aggregate(
            total_students=Count("pk", filter=Q(role="student")),
            total_staff=Count("pk", filter=Q(role__in=["hostel_office", "warden", "hmc"])),
        )
        
        category_stats = ComplaintCategory.objects.aggregate(
            total_categories=Count("pk")
        )

        return {
            **complaint_stats,
            **user_stats,
            **category_stats
        }
