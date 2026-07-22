from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.services.dashboard_service import DashboardService

from core.serializers.dashboard_serializers import (
    StudentDashboardSerializer,
)


class StudentDashboardAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        dashboard = (
            DashboardService.get_student_dashboard(
                request.user
            )
        )

        serializer = (
            StudentDashboardSerializer(
                {
                    "stats": dashboard["stats"],
                    "recent_complaints": dashboard[
                        "recent"
                    ],
                }
            )
        )

        return Response(
            serializer.data
        )