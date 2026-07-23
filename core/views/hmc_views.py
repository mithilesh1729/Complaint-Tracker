from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from core.models import Complaint, Hostel, ComplaintStatus, UserRole
from core.serializers import ComplaintListSerializer
from core.tasks import send_complaint_status_email_task

class IsHMC(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role == UserRole.HMC

class HMCDashboardAPIView(APIView):
    permission_classes = [IsHMC]

    def get(self, request):
        complaints = Complaint.objects.all()
        return Response({
            "stats": {
                "total_hostels": Hostel.objects.filter(is_active=True).count(),
                "total_escalated": complaints.filter(status=ComplaintStatus.ESCALATED_HMC).count(),
                "pending_overall": complaints.filter(status__in=[ComplaintStatus.PENDING, ComplaintStatus.IN_PROGRESS]).count(),
                "resolved_overall": complaints.filter(status=ComplaintStatus.RESOLVED).count(),
                "high_priority": complaints.filter(priority="high").exclude(status=ComplaintStatus.RESOLVED).count()
            }
        })

class HMCQueueAPIView(ListAPIView):
    permission_classes = [IsHMC]
    serializer_class = ComplaintListSerializer

    def get_queryset(self):
        return Complaint.objects.filter(
            status=ComplaintStatus.ESCALATED_HMC
        ).select_related("user", "category", "assigned_to").order_by("-created_at")

class HMCHostelPerformanceAPIView(APIView):
    permission_classes = [IsHMC]

    def get(self, request):
        hostels = Hostel.objects.filter(is_active=True)
        data = []
        for h in hostels:
            qs = Complaint.objects.filter(hostel=h.name)
            data.append({
                "hostel": h.name,
                "pending": qs.filter(status__in=[ComplaintStatus.PENDING, ComplaintStatus.IN_PROGRESS]).count(),
                "resolved": qs.filter(status=ComplaintStatus.RESOLVED).count(),
                "escalated": qs.filter(status=ComplaintStatus.ESCALATED_HMC).count()
            })
        return Response(data)

class HMCComplaintActionAPIView(APIView):
    permission_classes = [IsHMC]

    def post(self, request, complaint_id):
        action = request.data.get("action")
        remark = request.data.get("remark", "")
        
        complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
        
        if action == "return_warden":
            complaint.status = ComplaintStatus.ESCALATED_WARDEN
            message = "Complaint returned to Warden."
            if remark: 
                complaint.hmc_remark = remark
                message += f" Remark: {remark}"
            
        elif action == "close":
            complaint.status = ComplaintStatus.RESOLVED
            complaint.resolved_at = timezone.now()
            message = "Complaint closed and marked as Resolved."
            if remark: 
                complaint.hmc_remark = remark
                message += f" Remark: {remark}"
            
        elif action == "add_remark":
            message = "Remark added successfully."
            if remark: 
                complaint.hmc_remark = remark
                message = f"Remark added: {remark}"
            
        else:
            return Response({"detail": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
            
        complaint.save(update_fields=["status", "hmc_remark", "resolved_at"])
        
        from core.models import StatusLog
        StatusLog.objects.create(
            complaint=complaint,
            status=complaint.status,
            message=message
        )
        
        if action in ["return_warden", "close"]:
            send_complaint_status_email_task.delay(
                user_email=complaint.user.email,
                name=complaint.user.name,
                complaint_number=complaint.complaint_number,
                new_status=complaint.status,
                category_name=complaint.category.name,
            )
        
        return Response({"message": message})
