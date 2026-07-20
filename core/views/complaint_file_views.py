# download_complaint_slip

# complaint_logs

from django.http import FileResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import CanViewComplaint

from core.serializers.complaint_serializers import StatusLogSerializer

from core.selectors.complaint_selector import ComplaintSelector

from core.services.pdf_service import (
    generate_complaint_slip_pdf,
)



class ComplaintLogsAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanViewComplaint
        
    ]

    def get(
        self,
        request,
        complaint_id,
    ):

        complaint = (
            ComplaintSelector.get_complaint_or_404(
                complaint_id
            )
        )

        self.check_object_permissions(
            request,
            complaint,
        )

        logs = ComplaintSelector.list_status_logs(
            complaint
        )

        serializer = StatusLogSerializer(
            logs,
            many=True,
        )

        return Response(
            serializer.data
        )




class ComplaintSlipAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanViewComplaint
    ]

    def get(
        self,
        request,
        complaint_id,
    ):

        complaint = (
            ComplaintSelector.get_complaint_or_404(
                complaint_id
            )
        )

        self.check_object_permissions(
            request,
            complaint,
        )

        pdf = generate_complaint_slip_pdf(
            complaint
        )

        return FileResponse(

            pdf,

            as_attachment=True,

            filename=f"{complaint.complaint_number}.pdf",

            content_type="application/pdf",

        )