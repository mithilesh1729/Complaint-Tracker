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
from django.utils.decorators import method_decorator

from django.views.decorators.cache import cache_page

class OfficeDashboardAPIView(APIView):
    """
    Hostel Office dashboard summary.
    """

    permission_classes = [
        IsAuthenticated,
        IsHostelOffice,
    ]

    @method_decorator(cache_page(60))
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