from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Department
from core.serializers.student_serializers import DepartmentSerializer

from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import Department
from core.serializers.student_serializers import DepartmentSerializer

class DepartmentManagementAPIView(APIView):
    """
    CRUD for Departments (Admin only).
    Students can GET active departments.
    """
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get(self, request, department_id=None):
        if department_id:
            try:
                department = Department.objects.get(id=department_id)
                return Response(DepartmentSerializer(department).data)
            except Department.DoesNotExist:
                return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        search = request.query_params.get("search", "")
        
        # Admin sees all, others see only active
        if request.user.is_staff or request.user.is_superuser:
            departments = Department.objects.all()
        else:
            departments = Department.objects.filter(is_active=True)

        if search:
            departments = departments.filter(
                Q(name__icontains=search) | Q(code__icontains=search)
            )

        departments = departments.order_by("name")
        return Response(DepartmentSerializer(departments, many=True).data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
            # Toggle active status instead of hard delete
            department.is_active = not department.is_active
            department.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"detail": "Department not found"}, status=status.HTTP_404_NOT_FOUND)
