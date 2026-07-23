from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters, status
from django.core.cache import cache

from core.selectors.complaint_selector import ComplaintSelector
from core.serializers.complaint_serializers import ComplaintSerializer, ComplaintCategorySerializer
from core.models import Complaint

from core.selectors.complaint_list_selector import ComplaintListSelector
from core.selectors.category_selector import CategorySelector





from core.pagination import CustomPagination
from core.throttling import ComplaintRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from core.permissions import CanViewComplaint


# ComplaintListView
# ComplaintCreateAPIView
# ComplaintDetailAPIView
# ComplaintUpdateAPIView
# ComplaintDeleteAPIView
# ComplaintCategoryListAPIView


class ComplaintCreateAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = ComplaintSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        complaint = serializer.save()

        cache.delete(
            f"complaints_{request.user.roll_no}"
        )

        return Response(
            ComplaintSerializer(
                complaint,context={"request": request},
            ).data,
            status=status.HTTP_201_CREATED,
        )




class ComplaintDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        CanViewComplaint
    ]

    def get(self,request,complaint_id):
        complaint = (
            ComplaintSelector.get_complaint_or_404(
                complaint_id
            )
        )

        self.check_object_permissions(
            request,
            complaint,
        )

        serializer = ComplaintSerializer(
            complaint,
            context={"request": request},
        )

        return Response(
            serializer.data
        )


# Views → HTTP only.
# Services → Business rules.
# Selectors → Database queries.
# Models → Data.



class ComplaintDeleteAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]
    
    def delete(
        self,
        request,
        complaint_id,
    ):
        complaint = (
            ComplaintSelector.get_complaint_or_404(
                complaint_id
            )
        )
        if (
            complaint.user != request.user
            and
            not request.user.is_admin
        ):
            return Response(
                {
                    "detail":
                    "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        complaint.delete()
        cache.delete(
            f"complaints_{request.user.roll_no}"
        )
        return Response(
            {
                "message":
                "Complaint deleted successfully."
            }
        )



# Complaint List View
# =====================================================
class ComplaintListAPIView(generics.ListAPIView):
    """
    List complaints with:
    - Filtering
    - Pagination
    - Ordering
    - Rate limiting
    - Caching
    - Role-based access (Admin vs Student)

    JWT Authentication:
    - request.user is populated by JWTAuthentication
    """
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ComplaintRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    # Fields allowed for filtering
    filterset_fields = ['status', 'complaint_type', 'priority', 'user__roll_no']

    # Fields allowed for ordering
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        user = self.request.user

        # Using roll_no instead of user.id (custom primary key)
        cache_key = f"complaints_{user.roll_no}"

        cached_ids = cache.get(cache_key)
        if cached_ids:
            return Complaint.objects.filter(id__in=cached_ids)


        
        
        
        if user.is_admin:
            queryset = ComplaintListSelector.get_admin_complaints()
        else:
            queryset = ComplaintListSelector.get_student_complaints(user)
        cache.set(
            cache_key,
            list(queryset.values_list('id', flat=True)),
            timeout=60
        )

        return queryset

class ComplaintCategoryListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = CategorySelector.list_active_categories()

        serializer = ComplaintCategorySerializer(
            categories,
            many=True,
        )

        return Response(serializer.data)