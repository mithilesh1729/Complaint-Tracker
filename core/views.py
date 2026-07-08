from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, status
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend

from .models import Complaint, StatusLog, ComplaintImage, UserRole
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
  StudentCreateSerializer, StudentListSerializer, StudentUpdateSerializer  , StaffSerializer, ComplaintCategorySerializer, ProfileSerializer
);
from core.selectors.student_selector import StudentSelector
from core.services.student_service import StudentService
from core.models import Hostel


from core.services.complaint_service import ComplaintService
from core.services.user_service import UserService
from core.selectors.complaint_selector import ComplaintSelector




# # Complaint List View
# # =====================================================
# class ComplaintListView(generics.ListAPIView):
#     """
#     List complaints with:
#     - Filtering
#     - Pagination
#     - Ordering
#     - Rate limiting
#     - Caching
#     - Role-based access (Admin vs Student)

#     JWT Authentication:
#     - request.user is populated by JWTAuthentication
#     """
#     serializer_class = ComplaintSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = CustomPagination
#     throttle_classes = [ComplaintRateThrottle]
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

#     # Fields allowed for filtering
#     filterset_fields = ['status', 'complaint_type', 'priority', 'user__roll_no']

#     # Fields allowed for ordering
#     ordering_fields = ['created_at', 'updated_at']
#     ordering = ['-created_at']

#     def get_queryset(self):
#         user = self.request.user

#         # Using roll_no instead of user.id (custom primary key)
#         cache_key = f"complaints_{user.roll_no}"

#         cached_ids = cache.get(cache_key)
#         if cached_ids:
#             return Complaint.objects.filter(id__in=cached_ids)

#         # Admin sees all complaints
#         if user.is_admin:
#             queryset = Complaint.objects.all()
#         else:
#             queryset = Complaint.objects.filter(user=user)

#         # Cache complaint IDs for 1 minute
#         cache.set(
#             cache_key,
#             list(queryset.values_list('id', flat=True)),
#             timeout=60
#         )

#         return queryset


# Create Complaint
# =====================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complaint_create(request):
    serializer = ComplaintSerializer(
        data=request.data,
        context={"request": request},
    )

    serializer.is_valid(raise_exception=True)

    complaint = serializer.save()

    cache.delete(f"complaints_{request.user.roll_no}")

    return Response(
        ComplaintSerializer(complaint).data,
        status=status.HTTP_201_CREATED,
    )


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
def confirm_complaint_resolution(
    request,
    complaint_id,
):

    complaint = get_object_or_404(
        Complaint,
        complaint_id=complaint_id,
    )

    if complaint.user != request.user:
        return Response(
            {"detail":"Not allowed"},
            status=403,
        )

    if complaint.status != "resolved":
        return Response(
            {
                "detail":"Complaint not resolved."
            },
            status=400,
        )

    if complaint.is_confirmed:
        return Response(
            {
                "detail":"Already confirmed."
            },
            status=400,
        )

    ComplaintService.confirm_resolution(
        complaint=complaint,
        feedback=request.data.get(
            "feedback",
            "",
        ),
    )

    cache.delete(
        f"complaints_{request.user.roll_no}"
    )

    return Response(
        {
            "message":"Complaint confirmed."
        }
    )




# *******************************************************************************************

# class StudentAPIView(GenericAPIView):

#     permission_classes = [IsAdminUser]
#     pagination_class = StandardResultsSetPagination

#     def get(self, request, roll_no=None):

#         if roll_no:
#             student = StudentSelector.get_student_or_404(roll_no)

#             serializer = StudentListSerializer(student)

#             return Response(serializer.data)

#         queryset = StudentSelector.list_students(
#             search=request.query_params.get("search"),
#             department=request.query_params.get("department"),
#             hostel=request.query_params.get("hostel"),
#             is_active=request.query_params.get(
#                 "is_active",
#                 "true",
#             ).lower() == "true",
#         )

#         page = self.paginate_queryset(queryset)

#         serializer = StudentListSerializer(
#             page,
#             many=True,
#         )

#         return self.get_paginated_response(serializer.data)

#     def post(self, request):

#         serializer = StudentCreateSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         student = serializer.save()

#         return Response(
#             {
#                 "message": "Student created successfully.",
#                 "roll_no": student.roll_no,
#                 "temporary_password": student.temporary_password,
#             },
#             status=status.HTTP_201_CREATED,
#         )       
        
    
#     def patch(self, request, roll_no):

#         student = StudentSelector.get_student_or_404(roll_no)

#         serializer = StudentUpdateSerializer(
#             data=request.data,
#             partial=True,
#         )

#         serializer.is_valid(raise_exception=True)

#         data = serializer.validated_data

#         StudentService.update_student(
#             user=student,
#             name=data.get("name", student.name),
#             email=data.get("email", student.email),
#             phone_number=data.get(
#                 "phone_number",
#                 student.phone_number,
#             ),
#             department=data.get(
#                 "department",
#                 student.department,
#             ),
#         )

#         if (
#             "hostel" in data
#             or "room_no" in data
#         ):
#             StudentService.transfer_hostel(
#                 user=student,
#                 hostel=data.get("hostel", Hostel.objects.get(name=student.hostel)),
#                 room_no=data.get("room_no", student.room_no),
#             )

#         return Response(
#             {
#                 "message": "Student updated successfully."
#             }
#         )  
  
#     def delete(self, request, roll_no):

#         student = StudentSelector.get_student_or_404(roll_no)

#         StudentService.deactivate_student(student)

#         return Response(
#             {
#                 "message": "Student deactivated successfully."
#             }
#         )    
    
    



# class StudentResetPasswordAPIView(APIView):

#     permission_classes = [IsAdminUser]
    
#     def post(self, request, roll_no):
#         student = StudentSelector.get_student_or_404(roll_no)

#         password = StudentService.reset_password(student)
        
#         return Response(
#             {
#                 "temporary_password": password
#             }
#         ) 
        
        
# class HostelQueueAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         # Only Hostel Office users
#         if request.user.role != UserRole.HOSTEL_OFFICE:
#             return Response(
#                 {"detail": "Permission denied."},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         complaints = ComplaintSelector.list_hostel_queue(
#             hostel=request.user.hostel
#         )

#         serializer = ComplaintSerializer(
#             complaints,
#             many=True,
#         )

#         return Response(serializer.data)   
    
    
    


# class HostelQueueAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         if request.user.role != "hostel_office":
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         complaints = ComplaintSelector.list_hostel_queue(
#             hostel=request.user.hostel
#         )

#         serializer = ComplaintSerializer(
#             complaints,
#             many=True,
#         )

#         return Response(serializer.data)

    

# class AssignComplaintAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request, complaint_id):

#         if request.user.role != "hostel_office":
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         complaint = get_object_or_404(
#             Complaint,
#             complaint_id=complaint_id,
#         )

#         if complaint.assigned_to:
#             return Response(
#                 {"detail": "Already assigned."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         ComplaintService.assign_to_me(
#             complaint=complaint,
#             office_user=request.user,
#         )

#         return Response(
#             ComplaintSerializer(complaint).data
#         )   
        
 

# class MyAssignedComplaintsAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         complaints = ComplaintSelector.list_my_complaints(
#             request.user
#         )

#         serializer = ComplaintSerializer(
#             complaints,
#             many=True,
#         )

#         return Response(serializer.data)
    
    



# class StaffAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         if not request.user.is_admin:
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         staff = User.objects.filter(
#             role__in=[
#                 "hostel_office",
#                 "warden",
#                 "hmc",
#             ]
#         ).order_by("roll_no")

#         serializer = StaffSerializer(
#             staff,
#             many=True,
#         )

#         return Response(serializer.data)

#     def post(self, request):

#         if not request.user.is_admin:
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         serializer = StaffSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         staff = serializer.save()

#         return Response(
#             {
#                 "message": "Staff created successfully.",
#                 "roll_no": staff.roll_no,
#                 "temporary_password": serializer.temp_password,
#             },
#             status=status.HTTP_201_CREATED,
#         )    
                      



# class StaffResetPasswordAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, roll_no):

#         if not request.user.is_admin:
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         user = get_object_or_404(
#             User,
#             roll_no=roll_no,
#         )

#         # Safety check
#         if user.role not in [
#             "hostel_office",
#             "warden",
#             "hmc",
#         ]:
#             return Response(
#                 {"detail": "Not a staff account."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         temp_password = UserService.reset_password(user)

#         return Response(
#             {
#                 "message": "Password reset successfully.",
#                 "temporary_password": temp_password,
#             }
#         )
        
        

# class ComplaintCategoryListAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         categories = ComplaintSelector.list_active_categories()

#         serializer = ComplaintCategorySerializer(
#             categories,
#             many=True,
#         )

#         return Response(serializer.data)        
    
    
    
# class ResolveComplaintAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request, complaint_id):

#         complaint = get_object_or_404(
#             Complaint,
#             complaint_id=complaint_id,
#         )

#         if request.user.role != "hostel_office":
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         if complaint.assigned_to != request.user:
#             return Response(
#                 {
#                     "detail": "Complaint is not assigned to you."
#                 },
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         if complaint.status != "in_progress":
#             return Response(
#                 {
#                     "detail": "Only in-progress complaints can be resolved."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         ComplaintService.resolve_complaint(
#             complaint=complaint,
#             remark=request.data.get(
#                 "remark",
#                 "Complaint resolved.",
#             ),
#         )

#         cache.delete(
#             f"complaints_{complaint.user.roll_no}"
#         )

#         return Response(
#             ComplaintSerializer(complaint).data
#         )    
        
        
# class UpdateComplaintProgressAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def patch(self, request, complaint_id):

#         complaint = get_object_or_404(
#             Complaint,
#             complaint_id=complaint_id,
#         )

#         if request.user.role != "hostel_office":
#             return Response(
#                 {"detail": "Permission denied"},
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         if complaint.assigned_to != request.user:
#             return Response(
#                 {
#                     "detail": "This complaint is not assigned to you."
#                 },
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         if complaint.status != "in_progress":
#             return Response(
#                 {
#                     "detail": "Only in-progress complaints can be updated."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         ComplaintService.update_progress(
#             complaint=complaint,
#             priority=request.data.get(
#                 "priority",
#                 complaint.priority,
#             ),
#             remark=request.data.get(
#                 "remark",
#                 "Progress updated.",
#             ),
#         )

#         cache.delete(
#             f"complaints_{complaint.user.roll_no}"
#         )

#         return Response(
#             ComplaintSerializer(complaint).data,
#             status=status.HTTP_200_OK,
#         )
    
    
    

# class ReopenComplaintAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def post(self, request, complaint_id):

#         complaint = get_object_or_404(
#             Complaint,
#             complaint_id=complaint_id,
#         )

#         if complaint.user != request.user:
#             return Response(
#                 {
#                     "detail":"Not allowed"
#                 },
#                 status=status.HTTP_403_FORBIDDEN,
#             )

#         if complaint.status != "resolved":
#             return Response(
#                 {
#                     "detail":"Only resolved complaints can be reopened."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         ComplaintService.reopen_complaint(
#             complaint=complaint,
#             feedback=request.data.get(
#                 "feedback",
#                 "",
#             ),
#         )

#         cache.delete(
#             f"complaints_{request.user.roll_no}"
#         )

#         return Response(
#             ComplaintSerializer(complaint).data
#         )  
        
        
        
        
# class ProfileAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         serializer = ProfileSerializer(
#             request.user
#         )

#         return Response(serializer.data)      