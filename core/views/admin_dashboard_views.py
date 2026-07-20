from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from core.selectors.admin_dashboard_selector import AdminDashboardSelector
from core.serializers.admin_dashboard_serializers import AdminDashboardSerializer

class AdminDashboardAPIView(APIView):
    """
    Admin dashboard summary endpoint.
    """

    permission_classes = [
        IsAuthenticated,
        IsAdminUser,
    ]

    @method_decorator(cache_page(60))
    def get(self, request):
        dashboard = AdminDashboardSelector.get_dashboard()

        serializer = AdminDashboardSerializer(
            dashboard,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)
