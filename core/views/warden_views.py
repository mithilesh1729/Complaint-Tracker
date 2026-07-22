from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from core.models import Complaint, User, ComplaintStatus, UserRole
from core.pagination import StandardResultsSetPagination
from core.serializers import ComplaintListSerializer
from core.tasks import send_complaint_status_email_task

class IsWarden(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == UserRole.WARDEN

class WardenDashboardAPIView(APIView):
    permission_classes = [IsWarden]

    def get(self, request):
        hostel = request.user.hostel
        complaints = Complaint.objects.filter(hostel=hostel)
        today = timezone.now().date()
        
        return Response({
            "stats": {
                "pending": complaints.filter(status=ComplaintStatus.PENDING).count(),
                "escalated": complaints.filter(status=ComplaintStatus.ESCALATED_WARDEN).count(),
                "resolved_today": complaints.filter(status=ComplaintStatus.RESOLVED, resolved_at__date=today).count(),
                "overdue": complaints.filter(status=ComplaintStatus.PENDING).count(), # Simplified
                "office_staff": User.objects.filter(hostel=hostel, role=UserRole.HOSTEL_OFFICE, is_active=True).count(),
                "avg_resolution_time": "24h" # Placeholder for interview brevity
            }
        })


class WardenQueueAPIView(ListAPIView):
    permission_classes = [IsWarden]
    pagination_class = StandardResultsSetPagination
    serializer_class = ComplaintListSerializer

    def get_queryset(self):
        return Complaint.objects.filter(
            hostel=self.request.user.hostel, 
            status=ComplaintStatus.ESCALATED_WARDEN
        ).select_related("user", "category", "assigned_to").order_by("-created_at")


class WardenStaffPerformanceAPIView(APIView):
    permission_classes = [IsWarden]

    def get(self, request):
        staff = User.objects.filter(hostel=request.user.hostel, role=UserRole.HOSTEL_OFFICE)
        data = []
        for s in staff:
            assigned = Complaint.objects.filter(assigned_to=s).count()
            resolved = Complaint.objects.filter(assigned_to=s, status=ComplaintStatus.RESOLVED).count()
            pending = assigned - resolved
            data.append({
                "roll_no": s.roll_no,
                "name": s.name,
                "assigned": assigned,
                "resolved": resolved,
                "pending": pending,
            })
        return Response(data)


class WardenComplaintActionAPIView(APIView):
    permission_classes = [IsWarden]

    def post(self, request, complaint_id):
        action = request.data.get("action")
        remark = request.data.get("remark", "")
        
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id, hostel=request.user.hostel)
        
        if action == "send_back":
            complaint.status = ComplaintStatus.IN_PROGRESS
            message = "Complaint returned to Hostel Office."
            if remark: 
                complaint.warden_remark = remark
                message += f" Remark: {remark}"
            
        elif action == "escalate_hmc":
            complaint.status = ComplaintStatus.ESCALATED_HMC
            message = "Complaint escalated to HMC."
            if remark: 
                complaint.warden_remark = remark
                message += f" Remark: {remark}"
            
        elif action == "add_remark":
            message = "Remark added successfully."
            if remark: 
                complaint.warden_remark = remark
                message = f"Remark added: {remark}"
            
        else:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
            
        complaint.save(update_fields=["status", "warden_remark"])
        
        from core.models import StatusLog
        StatusLog.objects.create(
            complaint=complaint,
            status=complaint.status,
            message=message
        )
        
        if action in ["send_back", "escalate_hmc"]:
            send_complaint_status_email_task.delay(
                user_email=complaint.user.email,
                name=complaint.user.name,
                complaint_number=complaint.complaint_number,
                new_status=complaint.status,
                category_name=complaint.category.name,
            )
        
        return Response({"message": message})
