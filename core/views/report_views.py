import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from core.models import Complaint

class AdminReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="complaints_report.csv"'

        writer = csv.writer(response)
        
        writer.writerow([
            'Complaint ID', 
            'Student Roll No', 
            'Student Name',
            'Hostel', 
            'Room No', 
            'Category', 
            'Status', 
            'Priority',
            'Created At',
            'Resolved At'
        ])

        # Optimize query with select_related
        complaints = Complaint.objects.select_related('user', 'category').all().order_by('-created_at')

        for complaint in complaints:
            writer.writerow([
                complaint.complaint_number or complaint.complaint_id,
                complaint.user.roll_no if complaint.user else 'N/A',
                complaint.name,
                complaint.hostel,
                complaint.room_no,
                complaint.category.name if complaint.category else complaint.complaint_type,
                complaint.status,
                complaint.priority,
                complaint.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                complaint.resolved_at.strftime('%Y-%m-%d %H:%M:%S') if complaint.resolved_at else 'N/A'
            ])

        return response
