from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import ValidationError
from core.models import Complaint, StatusLog


class ComplaintService:
    """
    Business logic for Complaint Workflow.
    """

    @staticmethod
    @transaction.atomic
    def create_complaint(
        *,
        user,
        category,
        description,
        location_details,
        priority,
    ):
        """
        Student creates a complaint.
        """

        complaint = Complaint.objects.create(
            user=user,
            category=category,
            name=user.name,
            hostel=user.hostel,
            room_no=user.room_no,
            phone_number=user.phone_number,
            complaint_type=category.name,
            description=description,
            location_details=location_details,
            priority=priority,
            status="pending",
        )

        complaint.complaint_number = (
            f"CMP-{timezone.now().year}-{complaint.id:06d}"
        )

        complaint.save(
            update_fields=[
                "complaint_number",
            ]
        )

        StatusLog.objects.create(
            complaint=complaint,
            status="pending",
            message="Complaint submitted",
        )

        return complaint

    @staticmethod
    @transaction.atomic
    def assign_to_me(
        *,
        complaint,
        office_user,
        remark,
    ):
        """
        Hostel Office accepts responsibility.
        """

        if complaint.status != "pending":
            raise ValidationError(
                "Only pending complaints can be assigned."
            )

        if complaint.assigned_to:
            raise ValidationError(
                "Complaint is already assigned."
            )

        complaint.assigned_to = office_user
        complaint.status = "in_progress"
        complaint.updated_at = timezone.now()

        if hasattr(complaint, "latest_admin_remark"):
            complaint.latest_admin_remark = remark

            complaint.save(
                update_fields=[
                    "assigned_to",
                    "status",
                    "latest_admin_remark",
                    "updated_at",
                ]
            )
        else:
            complaint.save(
                update_fields=[
                    "assigned_to",
                    "status",
                    "updated_at",
                ]
            )

        StatusLog.objects.create(
            complaint=complaint,
            status="in_progress",
            message=remark,
        )

        return complaint

    @staticmethod
    @transaction.atomic
    def update_progress(
        *,
        complaint,
        priority,
        remark,
    ):
        """
        Office worker updates complaint progress.
        """

        if complaint.status != "in_progress":
            raise ValidationError(
                "Only complaints in progress can be updated."
            )

        complaint.priority = priority
        complaint.updated_at = timezone.now()

        if hasattr(complaint, "latest_admin_remark"):
            complaint.latest_admin_remark = remark

            complaint.save(
                update_fields=[
                    "priority",
                    "latest_admin_remark",
                    "updated_at",
                ]
            )
        else:
            complaint.save(
                update_fields=[
                    "priority",
                    "updated_at",
                ]
            )

        StatusLog.objects.create(
            complaint=complaint,
            status="in_progress",
            message=remark,
        )

        return complaint

    @staticmethod
    @transaction.atomic
    def resolve_complaint(
        *,
        complaint,
        remark,
    ):
        """
        Complaint resolved by Hostel Office.
        """

        if complaint.status != "in_progress":
            raise ValidationError(
                "Only complaints in progress can be resolved."
            )

        complaint.status = "resolved"
        complaint.resolved_at = timezone.now()
        complaint.updated_at = timezone.now()

        if hasattr(complaint, "latest_admin_remark"):
            complaint.latest_admin_remark = remark

            complaint.save(
                update_fields=[
                    "status",
                    "resolved_at",
                    "latest_admin_remark",
                    "updated_at",
                ]
            )
        else:
            complaint.save(
                update_fields=[
                    "status",
                    "resolved_at",
                    "updated_at",
                ]
            )

        StatusLog.objects.create(
            complaint=complaint,
            status="resolved",
            message=remark,
        )

        return complaint

    @staticmethod
    @transaction.atomic
    def confirm_resolution(
        *,
        complaint,
        feedback,
    ):
        """
        Student confirms resolution.
        """

        if complaint.status != "resolved":
            raise ValidationError(
                "Only resolved complaints can be confirmed."
            )

        complaint.is_confirmed = True
        complaint.confirmed_at = timezone.now()
        complaint.student_feedback = feedback
        complaint.closed_at = timezone.now()
        complaint.updated_at = timezone.now()

        complaint.save(
            update_fields=[
                "is_confirmed",
                "confirmed_at",
                "student_feedback",
                "closed_at",
                "updated_at",
            ]
        )

        StatusLog.objects.create(
            complaint=complaint,
            status="resolved",
            message="Resolution confirmed by student",
        )

        return complaint

    @staticmethod
    @transaction.atomic
    def reopen_complaint(
        *,
        complaint,
        feedback,
    ):
        """
        Student reopens a resolved complaint.

        The complaint remains assigned to the
        same Hostel Office worker.
        """

        if complaint.status != "resolved":
            raise ValidationError(
                "Only resolved complaints can be reopened."
            )

        complaint.status = "in_progress"
        complaint.student_feedback = feedback
        complaint.is_confirmed = False
        complaint.confirmed_at = None
        complaint.updated_at = timezone.now()

        complaint.save(
            update_fields=[
                "status",
                "student_feedback",
                "is_confirmed",
                "confirmed_at",
                "updated_at",
            ]
        )

        StatusLog.objects.create(
            complaint=complaint,
            status="in_progress",
            message=f"Reopened by student: {feedback}",
        )

        return complaint