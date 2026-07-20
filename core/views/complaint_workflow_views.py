# AssignComplaintAPIView

# MyAssignedComplaintsAPIView

# ResolveComplaintAPIView

# UpdateComplaintProgressAPIView



# ReopenComplaintAPIView

# HostelQueueAPIView

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated


from core.selectors.complaint_selector import ComplaintSelector


from core.services.complaint_service import ComplaintService
from core.serializers.complaint_serializers import ComplaintSerializer



from core.permissions import IsHostelOffice
from core.filters import ComplaintFilter
from core.pagination import ComplaintPagination
from core.selectors.complaint_list_selector import ComplaintListSelector
from core.serializers.complaint_list_serializers import ComplaintListSerializer


class ConfirmComplaintResolutionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, complaint_id):
        complaint = ComplaintSelector.get_complaint_or_404(complaint_id)

        if complaint.user != request.user:
            return Response(
                {"detail": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if complaint.status != "resolved":
            return Response(
                {"detail": "Only resolved complaints can be confirmed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.confirm_resolution(
            complaint=complaint,
            feedback=request.data.get("feedback", ""),
        )

        cache.delete(f"complaints_{request.user.roll_no}")

        return Response(
            ComplaintSerializer(complaint, context={"request": request}).data
        )

class ReopenComplaintAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, complaint_id):

        # complaint = get_object_or_404(
        #     Complaint,
        #     complaint_id=complaint_id,
        # )
        
        complaint = ComplaintSelector.get_complaint_or_404(
                complaint_id
        )

        if complaint.user != request.user:
            return Response(
                {
                    "detail":"Not allowed"
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if complaint.status != "resolved":
            return Response(
                {
                    "detail":"Only resolved complaints can be reopened."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.reopen_complaint(
            complaint=complaint,
            feedback=request.data.get(
                "feedback",
                "",
            ),
        )

        cache.delete(
            f"complaints_{request.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data
        )  
        
        
        
        
        
        
class UpdateComplaintProgressAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def patch(self, request, complaint_id):

        complaint = ComplaintSelector.get_complaint_or_404(
                complaint_id
        )

        if complaint.assigned_to != request.user:
            return Response(
                {
                    "detail": "This complaint is not assigned to you."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if complaint.status != "in_progress":
            return Response(
                {
                    "detail": "Only in-progress complaints can be updated."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        remark = request.data.get(
            "remark",
            "",
        ).strip()

        if not remark:
            return Response(
                {
                    "detail": "Progress remark is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.update_progress(
            complaint=complaint,
            priority=request.data.get(
                "priority",
                complaint.priority,
            ),
            remark=remark,
        )

        cache.delete(
            f"complaints_{complaint.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data,
            status=status.HTTP_200_OK,
        ) 






class ResolveComplaintAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def post(self, request, complaint_id):

        complaint = ComplaintSelector.get_complaint_or_404(
                complaint_id
        )

        if complaint.assigned_to != request.user:
            return Response(
                {
                    "detail": "Complaint is not assigned to you."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        if complaint.status != "in_progress":
            return Response(
                {
                    "detail": "Only in-progress complaints can be resolved."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        remark = request.data.get(
            "remark",
            "",
        ).strip()

        if not remark:
            return Response(
                {
                    "detail": "Resolution remark is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.resolve_complaint(
            complaint=complaint,
            remark=remark,
        )

        cache.delete(
            f"complaints_{complaint.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data
        )   
        
class EscalateToWardenAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def post(self, request, complaint_id):
        complaint = ComplaintSelector.get_complaint_or_404(complaint_id)

        if complaint.assigned_to != request.user:
            return Response({"detail": "Complaint is not assigned to you."}, status=status.HTTP_403_FORBIDDEN)

        if complaint.status != "in_progress":
            return Response({"detail": "Only in-progress complaints can be escalated."}, status=status.HTTP_400_BAD_REQUEST)

        remark = request.data.get("remark", "").strip()

        from core.models import ComplaintStatus, StatusLog
        complaint.status = ComplaintStatus.ESCALATED_WARDEN
        complaint.save(update_fields=["status"])
        
        StatusLog.objects.create(
            complaint=complaint,
            status=ComplaintStatus.ESCALATED_WARDEN,
            message=f"Escalated to Warden by {request.user.name}. Remark: {remark}"
        )

        cache.delete(f"complaints_{complaint.user.roll_no}")
        return Response(ComplaintSerializer(complaint,context={"request": request},).data)

class AssignComplaintAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def post(self, request, complaint_id):

        complaint = ComplaintSelector.get_complaint_or_404(
                    complaint_id
        )

        if complaint.assigned_to:
            return Response(
                {"detail": "Already assigned."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if complaint.status != "pending":
            return Response(
                {
                    "detail": "Only pending complaints can be assigned.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )    

        remark = request.data.get(
            "remark",
            "",
        ).strip()

        if not remark:
            return Response(
                {
                    "detail": "Initial remark is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.assign_to_me(
            complaint=complaint,
            office_user=request.user,
            remark=remark,
        )

        cache.delete(
            f"complaints_{complaint.user.roll_no}"
        )
        
        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data
        )   
        
        
        
        
class HostelQueueAPIView(APIView):
    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def get(self, request):

        complaints = ComplaintListSelector.get_office_queue(
            hostel=request.user.hostel
        )

        serializer = ComplaintSerializer(
            complaints,
            context={"request": request},
            many=True,
        )

        return Response(serializer.data)          





class OfficeAssignedComplaintsAPIView(ListAPIView):
    """
    Complaints assigned to the current office user.
    """

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    serializer_class = ComplaintListSerializer

    pagination_class = ComplaintPagination

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
        return ComplaintListSelector.get_assigned_complaints(
            self.request.user,
        )   
               