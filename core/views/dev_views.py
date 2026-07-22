from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from core.models import EmailLog

class EmailLogAPIView(APIView):
    """
    Returns the last 50 emails sent by the system.
    Only accessible by Admin Users.
    Useful for development/testing when SMTP is disabled or using Mailtrap.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        logs = EmailLog.objects.all().order_by("-created_at")[:50]
        data = [
            {
                "id": log.id,
                "recipient": log.recipient,
                "subject": log.subject,
                "body": log.body,
                "sent_at": log.created_at,
            }
            for log in logs
        ]
        return Response(data)
