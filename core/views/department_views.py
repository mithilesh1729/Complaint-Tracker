from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Department
from core.serializers.student_serializers import DepartmentSerializer

class DepartmentListAPIView(APIView):
    """
    Returns a list of all active departments.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.filter(is_active=True).order_by("name")
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
