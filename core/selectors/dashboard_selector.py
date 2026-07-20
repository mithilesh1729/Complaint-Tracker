from core.models import Complaint


class DashboardSelector:
    """
    Read-only queries for Student Dashboard.
    """

    @staticmethod
    def get_student_dashboard_data(user):
        complaints = (
            Complaint.objects
            .for_user(user)
        )

        return {
            "stats": complaints.dashboard_stats(),

            "recent": (
                complaints
                .with_related()
                .latest()[:5]
            ),
        }