from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from django.shortcuts import get_object_or_404

from core.models import Hostel
from core.serializers import HostelSerializer

class HostelManagementAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, hostel_id=None):
        if hostel_id:
            hostel = get_object_or_404(Hostel, id=hostel_id)
            serializer = HostelSerializer(hostel)
            return Response(serializer.data)
            
        hostels = Hostel.objects.all().order_by("name")
        
        search = request.query_params.get("search")
        if search:
            hostels = hostels.filter(name__icontains=search)
            
        serializer = HostelSerializer(hostels, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HostelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Hostel created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    def patch(self, request, hostel_id):
        hostel = get_object_or_404(Hostel, id=hostel_id)
        serializer = HostelSerializer(hostel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Hostel updated successfully", "data": serializer.data}
        )

    def delete(self, request, hostel_id):
        hostel = get_object_or_404(Hostel, id=hostel_id)
        hostel.is_active = not hostel.is_active
        hostel.save()
        action = "activated" if hostel.is_active else "deactivated"
        return Response(
            {"message": f"Hostel {action} successfully"}
        )
