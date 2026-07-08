

from django.db.models import Q

from core.models import Complaint, ComplaintCategory
from django.shortcuts import get_object_or_404

class ComplaintSelector:
    """
    Read-only queries for Complaint module.
    """

    @staticmethod
    def get_complaint(complaint_id):
        return (
            Complaint.objects
            .select_related(
                "user",
                "category",
                "assigned_to",
            )
            .prefetch_related(
                "images",
                "status_logs",
            )
            .get(complaint_id=complaint_id)
        )

    @staticmethod
    def list_student_complaints(user):

        return (
            Complaint.objects
            .filter(user=user)
            .select_related("category")
            .order_by("-created_at")
        )

    @staticmethod
    def list_hostel_queue(hostel):
        return (
            Complaint.objects.filter(
                hostel=hostel,
                status="pending",
                assigned_to__isnull=True,
            )
            .select_related(
                "user",
                "category",
            )
            .order_by("-created_at")
        )

    @staticmethod
    def list_assigned_to_me(user):

        return (
            Complaint.objects
            .filter(
                assigned_to=user,
            )
            .select_related(
                "user",
                "category",
            )
            .order_by("-updated_at")
        )

    @staticmethod
    def search(queryset, search):

        if not search:
            return queryset

        return queryset.filter(
            Q(name__icontains=search)
            |
            Q(description__icontains=search)
            |
            Q(complaint_number__icontains=search)
        )

    @staticmethod
    def filter_status(queryset, status):

        if not status:
            return queryset

        return queryset.filter(status=status)

    @staticmethod
    def filter_category(queryset, category):

        if not category:
            return queryset

        return queryset.filter(category__id=category)
    
    @staticmethod
    def list_active_categories():

        return (
            ComplaintCategory.objects.filter(
                is_active=True
            )
            .order_by(
                "display_order",
                "name",
            )
        )
        
    @staticmethod
    def list_my_complaints(user):

        return (
            Complaint.objects.filter(
                assigned_to=user,
            )
            .select_related(
                "user",
                "category",
            )
            .order_by("-created_at")
        )    
    
    @staticmethod
    def get_complaint_or_404(complaint_id):
        return get_object_or_404(
            Complaint,
            complaint_id=complaint_id,
        )
        
    @staticmethod
    def list_status_logs(complaint):
        return complaint.status_logs.order_by(
            "timestamp"
        )    
   
        