#  necessary Django and DRF modules
from django.contrib.auth import logout, authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters
from django.core.cache import cache
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from .models import Complaint, StatusLog, ComplaintImage
from .serializers import ComplaintSerializer
from .pagination import CustomPagination
from .throttling import ComplaintRateThrottle
from django.contrib.auth import get_user_model

User = get_user_model()

# ✅ Session-Based Login Endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Handles user login using session-based authentication.
    - Takes roll_no and password from request data.
    - Authenticates user and creates a session if credentials are valid.
    - Returns success message with instructions to use cookies for subsequent requests.
    """
    roll_no = request.data.get('roll_no')
    password = request.data.get('password')

    if not roll_no or not password:
        return Response({"error": "Roll number and password are required"}, status=400)

    user = authenticate(request, roll_no=roll_no, password=password)
    if user is not None:
        login(request, user)
        return Response({
            "message": "Login successful",
            "info": "Use cookies (csrftoken, sessionid) for authenticated requests"
        }, status=200)
    return Response({"error": "Invalid credentials"}, status=401)

# ✅ Session-Based Logout Endpoint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logs out the user by clearing their session.
    - Ends the current session using Django's built-in logout function.
    - Returns a success message.
    """
    logout(request)
    return Response({"message": "Logout successful"}, status=200)

# ✅ Complaint List View with Advanced Features
class ComplaintListView(generics.ListAPIView):
    """
    Retrieve a list of complaints with advanced features:
    - Filtering: Filter by status, complaint_type, priority, or user roll_no.
    - Pagination: Custom pagination for manageable response sizes.
    - Throttling: Rate limiting to prevent abuse.
    - Ordering: Sort by created_at or updated_at timestamps.
    - Caching: Cache results for 1 minute to improve performance.
    - Role-Based Access: Admins see all complaints; students see only their own.
    """
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    throttle_classes = [ComplaintRateThrottle]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
    # ✅ Define fields that can be filtered
    filterset_fields = ['status', 'complaint_type', 'priority', 'user__roll_no']
    
    # ✅ Define fields that can be used for ordering
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # Default: Newest complaints first

    def get_queryset(self):
        """
        Returns the queryset of complaints based on user role:
        - Admins: All complaints in the system.
        - Students: Only their own complaints.
        - Applies caching using roll_no as cache key (since roll_no is the primary key).
        """
        user = self.request.user
        # Use roll_no instead of id since roll_no is the primary key
        cache_key = f"complaints_{user.roll_no}"

        # ✅ Try fetching from cache first
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Complaint.objects.filter(id__in=cached_data)

        # ✅ Fetch from database if not cached
        if user.is_admin:
            queryset = Complaint.objects.all()
        else:
            queryset = Complaint.objects.filter(user=user)
        
        # ✅ Cache the IDs of the queryset for 1 minute
        cache.set(cache_key, list(queryset.values_list('id', flat=True)), timeout=60)
        
        return queryset

# ✅ Create Complaint
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complaint_create(request):
    serializer = ComplaintSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user

        if request.user.is_admin and 'roll_no' in request.data:
            user = User.objects.filter(roll_no=request.data['roll_no']).first()
            if not user:
                return Response({"error": "User with this roll number does not exist"}, status=400)

        if request.data.get('complaint_type') not in dict(Complaint.TYPE_CHOICES):
            return Response({"error": "Invalid complaint type"}, status=400)

        complaint = serializer.save(user=user)

        images = request.FILES.getlist('images')
        for image in images:
            ComplaintImage.objects.create(complaint=complaint, image=image)

        cache.delete(f"complaints_{request.user.id}")  # Invalidate cache
        return Response(ComplaintSerializer(complaint).data, status=201)
    
    return Response(serializer.errors, status=400)

# ✅ Retrieve Single Complaint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complaint_detail(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    if not request.user.is_admin and complaint.user != request.user:
        return Response({"error": "You can only view your own complaints"}, status=403)
    
    return Response(ComplaintSerializer(complaint).data)

# ✅ Update Complaint (Only Admin)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complaint_update(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)

    if not request.user.is_admin:
        return Response({"error": "Only admins can update complaints"}, status=403)
    
    serializer = ComplaintSerializer(complaint, data=request.data, partial=True)
    if serializer.is_valid():
        old_status = complaint.status
        complaint = serializer.save()

        if 'status' in request.data and complaint.status != old_status:
            message = request.data.get('message', 'Status updated')
            StatusLog.objects.create(complaint=complaint, status=complaint.status, message=message)

        cache.delete(f"complaints_{request.user.id}")  # Invalidate cache
        return Response(serializer.data)
    
    return Response(serializer.errors, status=400)

# ✅ Delete Complaint
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def complaint_delete(request, complaint_id):
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    
    if complaint.user != request.user and not request.user.is_admin:
        return Response({"error": "You can only delete your own complaints"}, status=403)
    
    complaint.delete()
    cache.delete(f"complaints_{request.user.id}")  # Invalidate cache
    return Response({"message": "Complaint deleted successfully"}, status=200)
