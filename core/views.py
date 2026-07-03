from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from .models import Complaint, StatusLog, ComplaintImage
from .serializers import ComplaintSerializer
from .pagination import CustomPagination
from .throttling import ComplaintRateThrottle
from django.contrib.auth import get_user_model

from django.http import HttpResponse
from .services.pdf_service import generate_complaint_slip_pdf
from django.utils import timezone

from .permissions import IsOwnerOrAdmin

User = get_user_model()


# from rest_framework import status
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from core.pagination import StandardResultsSetPagination


from .serializers import (
  StudentCreateSerializer, StudentListSerializer, StudentUpdateSerializer  
);
from core.selectors.student_selector import StudentSelector
from core.services.student_service import StudentService
from core.models import Hostel




# Complaint List View
# =====================================================
class ComplaintListView(generics.ListAPIView):
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
    pagination_class = CustomPagination
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

        # Admin sees all complaints
        if user.is_admin:
            queryset = Complaint.objects.all()
        else:
            queryset = Complaint.objects.filter(user=user)

        # Cache complaint IDs for 1 minute
        cache.set(
            cache_key,
            list(queryset.values_list('id', flat=True)),
            timeout=60
        )

        return queryset


# Create Complaint
# =====================================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complaint_create(request):
    serializer = ComplaintSerializer(
        data=request.data,
        context={'request': request}
    )

    if serializer.is_valid():
        user = request.user

        # Admin can create complaint on behalf of student
        if user.is_admin and 'roll_no' in request.data:
            user = User.objects.filter(roll_no=request.data['roll_no']).first()
            if not user:
                return Response(
                    {"error": "User with this roll number does not exist"},
                    status=400
                )

        # Validate complaint type
        if request.data.get('complaint_type') not in dict(Complaint.TYPE_CHOICES):
            return Response({"error": "Invalid complaint type"}, status=400)

        complaint = serializer.save(user=user)

        # image uploads
        images = request.FILES.getlist('images')
        for image in images:
            ComplaintImage.objects.create(
                complaint=complaint,
                image=image
            )

        # Invalidate cache using roll_no instead of user.id
        cache.delete(f"complaints_{request.user.roll_no}")

        return Response(
            ComplaintSerializer(complaint).data,
            status=201
        )

    return Response(serializer.errors, status=400)


# Retrieve Single Complaint
# =====================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsOwnerOrAdmin])
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    # ✅ Explicit permission check (correct for FBV)
    for permission in request.resolver_match.func.permission_classes:
        perm = permission()
        if hasattr(perm, "has_object_permission"):
            if not perm.has_object_permission(request, None, complaint):
                return Response({"error": "You can only view your own complaints"}, status=403)

    return Response(ComplaintSerializer(complaint).data)


# Update Complaint (Admin Only)
# =====================================================
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complaint_update(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    if not request.user.is_admin:
        return Response(
            {"error": "Only admins can update complaints"},
            status=403
        )

    serializer = ComplaintSerializer(
        complaint,
        data=request.data,
        partial=True
    )

    if serializer.is_valid():
        old_status = complaint.status
        
        # Attach transient admin remark for signal
        complaint._status_change_message = request.data.get(
            "message",
            "Status updated by admin"
        )
        
        complaint = serializer.save()
        # Cache invalidation using roll_no
        cache.delete(f"complaints_{request.user.roll_no}")

        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# Delete Complaint
# =====================================================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def complaint_delete(request, complaint_id):
    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id
    )

    if complaint.user != request.user and not request.user.is_admin:
        return Response(
            {"error": "You can only delete your own complaints"},
            status=403
        )

    complaint.delete()

    # Cache invalidation using roll_no
    cache.delete(f"complaints_{request.user.roll_no}")

    return Response(
        {"message": "Complaint deleted successfully"},
        status=200
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def complaint_logs(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    # Admin OR owner can view logs
    if not request.user.is_admin and complaint.user != request.user:
        return Response({"error": "Forbidden"}, status=403)

    logs = complaint.status_logs.order_by("timestamp")

    data = [
        {
            "status": log.status,
            "message": log.message,
            "timestamp": log.timestamp,
        }
        for log in logs
    ]

    return Response(data)






from django.http import FileResponse
from .services.pdf_service import generate_complaint_slip_pdf


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def download_complaint_slip(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    # Admin OR complaint owner allowed
    if not request.user.is_admin and complaint.user != request.user:
        return Response({"detail": "Not allowed"}, status=403)

    pdf_buffer = generate_complaint_slip_pdf(complaint)

    return FileResponse(
        pdf_buffer,
        as_attachment=True,
        filename=f"complaint_{complaint.complaint_id}.pdf",
        content_type="application/pdf",
    )



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_complaint_resolution(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    # Only owner
    if complaint.user != request.user:
        return Response({"detail": "Not allowed"}, status=403)

    # ❌ Must be resolved
    if complaint.status != "resolved":
        return Response(
            {"detail": "Complaint not resolved yet"},
            status=400
        )

    # Idempotent
    if complaint.is_confirmed:
        return Response(
            {"detail": "Already confirmed"},
            status=200
        )

    # Confirm
    complaint.is_confirmed = True
    complaint.confirmed_at = timezone.now()
    complaint.student_feedback = request.data.get("feedback", "")
    complaint.save()

    StatusLog.objects.create(
        complaint=complaint,
        status="resolved",
        message="Resolution confirmed by student"
    )

    return Response(
        {"message": "Resolution confirmed"},
        status=200
    )
    



# *******************************************************************************************

class StudentAPIView(GenericAPIView):

    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def get(self, request, roll_no=None):

        if roll_no:
            student = StudentSelector.get_student_or_404(roll_no)

            serializer = StudentListSerializer(student)

            return Response(serializer.data)

        queryset = StudentSelector.list_students(
            search=request.query_params.get("search"),
            department=request.query_params.get("department"),
            hostel=request.query_params.get("hostel"),
            is_active=request.query_params.get(
                "is_active",
                "true",
            ).lower() == "true",
        )

        page = self.paginate_queryset(queryset)

        serializer = StudentListSerializer(
            page,
            many=True,
        )

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = StudentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        student = serializer.save()

        return Response(
            {
                "message": "Student created successfully.",
                "roll_no": student.roll_no,
                "temporary_password": student.temporary_password,
            },
            status=status.HTTP_201_CREATED,
        )       
        
    
    def patch(self, request, roll_no):

        student = StudentSelector.get_student_or_404(roll_no)

        serializer = StudentUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        StudentService.update_student(
            user=student,
            name=data.get("name", student.name),
            email=data.get("email", student.email),
            phone_number=data.get(
                "phone_number",
                student.phone_number,
            ),
            department=data.get(
                "department",
                student.department,
            ),
        )

        if (
            "hostel" in data
            or "room_no" in data
        ):
            StudentService.transfer_hostel(
                user=student,
                hostel=data.get("hostel", Hostel.objects.get(name=student.hostel)),
                room_no=data.get("room_no", student.room_no),
            )

        return Response(
            {
                "message": "Student updated successfully."
            }
        )  
  
    def delete(self, request, roll_no):

        student = StudentSelector.get_student_or_404(roll_no)

        StudentService.deactivate_student(student)

        return Response(
            {
                "message": "Student deactivated successfully."
            }
        )    
    
    



class StudentResetPasswordAPIView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request, roll_no):

        student = StudentSelector.get_student_or_404(roll_no)

        password = StudentService.reset_password(student)

        return Response(
            {
                "temporary_password": password
            }
        )        
