from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsHostelOffice

from core.selectors.office_dashboard_selector import (
    OfficeDashboardSelector,
)

from core.serializers.office_dashboard_serializers import (
    OfficeDashboardSerializer,
)

class OfficeDashboardAPIView(APIView):
    """
    Hostel Office dashboard summary.
    """

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    def get(self, request):
        dashboard = (
            OfficeDashboardSelector.get_dashboard(
                request.user,
            )
        )

        serializer = OfficeDashboardSerializer(
            dashboard,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)