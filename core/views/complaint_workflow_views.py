# AssignComplaintAPIView

# MyAssignedComplaintsAPIView

# ResolveComplaintAPIView

# UpdateComplaintProgressAPIView

# ConfirmComplaintResolutionAPIView

# ReopenComplaintAPIView

# HostelQueueAPIView

from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import UserRole
from core.selectors.complaint_selector import ComplaintSelector
from core.services.complaint_service import ComplaintService
from core.serializers.complaint_serializers import ComplaintSerializer



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

    permission_classes = [IsAuthenticated]

    def patch(self, request, complaint_id):

        complaint = ComplaintSelector.get_complaint_or_404(
                complaint_id
        )

        if request.user.role != UserRole.HOSTEL_OFFICE:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
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

        ComplaintService.update_progress(
            complaint=complaint,
            priority=request.data.get(
                "priority",
                complaint.priority,
            ),
            remark=request.data.get(
                "remark",
                "Progress updated.",
            ),
        )

        cache.delete(
            f"complaints_{complaint.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data,
            status=status.HTTP_200_OK,
        ) 






class ResolveComplaintAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, complaint_id):

        complaint = ComplaintSelector.get_complaint_or_404(
                complaint_id
        )

        if request.user.role != UserRole.HOSTEL_OFFICE:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
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

        ComplaintService.resolve_complaint(
            complaint=complaint,
            remark=request.data.get(
                "remark",
                "Complaint resolved.",
            ),
        )

        cache.delete(
            f"complaints_{complaint.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data
        )   
        
        

class AssignComplaintAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, complaint_id):

        if request.user.role != UserRole.HOSTEL_OFFICE:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        complaint = ComplaintSelector.get_complaint_or_404(
                    complaint_id
        )

        if complaint.assigned_to:
            return Response(
                {"detail": "Already assigned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ComplaintService.assign_to_me(
            complaint=complaint,
            office_user=request.user,
        )

        return Response(
            ComplaintSerializer(complaint,context={"request": request},).data
        )   
        
        
        
        
class HostelQueueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Only Hostel Office users
        if request.user.role != UserRole.HOSTEL_OFFICE:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN,
            )

        complaints = ComplaintSelector.list_hostel_queue(
            hostel=request.user.hostel
        )

        serializer = ComplaintSerializer(
            complaints,
            context={"request": request},
            many=True,
        )

        return Response(serializer.data)          


class MyAssignedComplaintsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        complaints = ComplaintSelector.list_my_complaints(
            request.user
        )

        serializer = ComplaintSerializer(
            complaints,
            context={"request": request},
            many=True,
        )

        return Response(serializer.data)                