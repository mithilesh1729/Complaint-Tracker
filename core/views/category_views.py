from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.models import ComplaintCategory
from core.serializers import ComplaintCategorySerializer

class CategoryManagementAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id=None):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        if category_id:
            category = get_object_or_404(ComplaintCategory, id=category_id)
            serializer = ComplaintCategorySerializer(category)
            return Response(serializer.data)

        categories = ComplaintCategory.objects.all().order_by("display_order", "name")
        serializer = ComplaintCategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ComplaintCategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, category_id):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        category = get_object_or_404(ComplaintCategory, id=category_id)
        serializer = ComplaintCategorySerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, category_id):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        category = get_object_or_404(ComplaintCategory, id=category_id)
        # Soft delete
        category.is_active = not category.is_active
        category.save(update_fields=["is_active"])
        return Response({"message": f"Category {'activated' if category.is_active else 'deactivated'} successfully."})
