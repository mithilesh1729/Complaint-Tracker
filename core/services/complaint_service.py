# Complaint Workflow Module
# │
# ├── Phase 1
# │   Refactor Student Complaint Form
# │   (Auto-fill profile data)
# │
# ├── Phase 2
# │   Complaint Service
# │   ├── create_complaint()
# │   ├── assign_to_me()
# │   ├── update_progress()
# │   ├── resolve()
# │   ├── confirm()
# │   └── reopen()
# │
# ├── Phase 3
# │   Hostel Office Dashboard
# │   (Only hostel complaints)
# │
# ├── Phase 4
# │   Student Dashboard
# │   (Confirmation / Reject)
# │
# ├── Phase 5
# │   Warden Dashboard
# │
# └── Phase 6
#     HMC Dashboard + Analytics





#                          SUPER ADMIN
#                               │
#                               │
#       Creates Hostels, Departments, Categories,
#       Hostel Office Users, Wardens, HMC Users
#                               │
# ────────────────────────────────────────────────────────────

#                         STUDENT LOGIN
#                               │
#                               ▼
#                    Click "Raise Complaint"
#                               │
#                               ▼
#                  Fill ONLY these fields

#                  • Complaint Category
#                  • Description
#                  • Location Details
#                  • Images (Optional)

#           (Everything else comes from DB)

#       Name ✔
#       Roll No ✔
#       Hostel ✔
#       Room ✔
#       Department ✔
#       Phone ✔

#                               │
#                               ▼
#                     Complaint Submitted
#                Status = "Pending"

#                               │
#                               ▼
#         Automatically visible to ONLY that Hostel Office

# ────────────────────────────────────────────────────────────

#                   HOSTEL OFFICE DASHBOARD

#           Sees complaints of THEIR hostel only

#                               │
#                               ▼
#                      Open Complaint
#                               │
#                               ▼
#                  "Assign To Me" (Office Worker)

#         assigned_to = current office worker

#                               │
#                               ▼
#                  Status → In Progress

#                               │
#                               ▼
#                Write Remarks (multiple times)

#                               │
#                               ▼
#           Upload Resolution Photo (optional)

#                               │
#                               ▼
#                  Status → Resolved

#                               │
#                               ▼
#         Student Confirmation Required

# ────────────────────────────────────────────────────────────

#                      STUDENT DASHBOARD

# Notification:

# "Your complaint has been resolved."

#                               │
#                 ┌─────────────┴─────────────┐
#                 │                           │
#                 ▼                           ▼
#           Confirm                     Reject
#                 │                           │
#                 ▼                           ▼
#        Complaint Closed             Back to Hostel Office
#                                     Status = In Progress
#                                     Student Feedback Saved

# ────────────────────────────────────────────────────────────

#                       HOSTEL WARDEN

# Does NOT work on complaints.

# Can only monitor

# • Pending
# • Long Pending
# • Resolved
# • Reopened

# ────────────────────────────────────────────────────────────

#                             HMC

# Sees

# • Overall Analytics
# • Hostel Performance
# • Resolution Time
# • Complaint Trends


# *********************************************************************************************

from django.db import transaction
from django.utils import timezone

from core.models import Complaint, StatusLog


from django.db.models import Max
from datetime import datetime

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
    ):
        """
        Hostel office worker accepts responsibility.
        """

        complaint.assigned_to = office_user
        complaint.status = "in_progress"

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
            message=f"Assigned to {office_user.name}",
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

        complaint.priority = priority

        complaint.save(
            update_fields=[
                "priority",
                "updated_at",
            ]
        )

        StatusLog.objects.create(
            complaint=complaint,
            status=complaint.status,
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
        Complaint resolved by office worker.
        """

        complaint.status = "resolved"
        complaint.resolved_at = timezone.now()

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
        Student accepts resolution.
        """

        complaint.is_confirmed = True
        complaint.confirmed_at = timezone.now()
        complaint.student_feedback = feedback
        complaint.closed_at = timezone.now()

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
        Student rejects resolution.
        """

        complaint.status = "in_progress"
        complaint.student_feedback = feedback
        complaint.is_confirmed = False

        complaint.save(
            update_fields=[
                "status",
                "student_feedback",
                "is_confirmed",
                "updated_at",
            ]
        )

        StatusLog.objects.create(
            complaint=complaint,
            status="in_progress",
            message=f"Reopened by student: {feedback}",
        )

        return complaint
    
    










