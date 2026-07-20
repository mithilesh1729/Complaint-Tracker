from core.models import Complaint


class ComplaintListSelector:
    """
    Read-only selectors for complaint listing pages.
    """

    @classmethod
    def get_student_complaints(cls, user):
        return (
            Complaint.objects
            .for_user(user)
            .with_related()
            .prefetch_related("images", "status_logs")
            .latest()
        )

    @classmethod
    def get_office_queue(cls):
        return (
            Complaint.objects
            .pending()
            .unassigned()
            .with_related()
            .prefetch_related("images", "status_logs")
            .latest()
        )

    @classmethod
    def get_assigned_complaints(cls, user):
        return (
            Complaint.objects
            .assigned_to(user)
            .with_related()
            .prefetch_related("images", "status_logs")
            .latest()
        )

    @classmethod
    def get_admin_complaints(cls):
        return (
            Complaint.objects
            .with_related()
            .latest()
        )

    @classmethod
    def get_warden_queue(cls):
        return (
            Complaint.objects
            .with_related()
            .latest()
        )

    @classmethod
    def get_hmc_queue(cls):
        return (
            Complaint.objects
            .with_related()
            .latest()
        )