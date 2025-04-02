from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Complaint, StatusLog, ComplaintImage
from .serializers import ComplaintSerializer
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


User = get_user_model()

# ✅ Retrieve All Complaints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complaint_list(request):
    """
    Retrieve complaints.
    - Admins: View all complaints.
    - Users: View only their own complaints.
    """
    complaints = Complaint.objects.all() if request.user.is_admin else Complaint.objects.filter(user=request.user)
    serializer = ComplaintSerializer(complaints, many=True)
    return Response(serializer.data)

# # ✅ Create Complaint
# @api_view(['POST'])
# @csrf_exempt  # Disable CSRF for this view
# @permission_classes([IsAuthenticated])
# def complaint_create(request):
#     """
#     Create a complaint with optional images.
#     - Regular users create their own complaints.
#     - Admins can create complaints for students using 'roll_no'.
#     """
#     serializer = ComplaintSerializer(data=request.data, context={'request': request})
    
#     if serializer.is_valid():
#         user = request.user
#         if request.user.is_admin and 'roll_no' in request.data:
#             user = User.objects.filter(roll_no=request.data['roll_no']).first()
#             if not user:
#                 return Response({"error": "User with this roll number does not exist"}, status=400)

#         # Validate complaint_type
#         if request.data.get('complaint_type') not in dict(Complaint.TYPE_CHOICES):
#             return Response({"error": "Invalid complaint type"}, status=400)

#         complaint = serializer.save(user=user)
        
#         # Handle image uploads
#         images = request.FILES.getlist('images')
#         for image in images:
#             ComplaintImage.objects.create(complaint=complaint, image=image)
        
#         serializer = ComplaintSerializer(complaint)
#         return Response(serializer.data, status=201)
    
#     return Response(serializer.errors, status=400)




@api_view(['POST'])
@csrf_exempt  # Disable CSRF for this view
@permission_classes([IsAuthenticated])
def complaint_create(request):
    """
    Create a complaint with optional images.
    - Regular users create their own complaints.
    - Admins can create complaints for students using 'roll_no'.
    """
    serializer = ComplaintSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = request.user
        # Admin can create complaints for students by roll_no
        if request.user.is_admin and 'roll_no' in request.data:
            user = User.objects.filter(roll_no=request.data['roll_no']).first()
            if not user:
                return Response({"error": "User with this roll number does not exist"}, status=400)

        # Validate complaint_type
        if request.data.get('complaint_type') not in dict(Complaint.TYPE_CHOICES):
            return Response({"error": "Invalid complaint type"}, status=400)

        # Save the complaint object
        complaint = serializer.save(user=user)
        
        # Handle image uploads if any
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                ComplaintImage.objects.create(complaint=complaint, image=image)
        
        # Return the serialized complaint data
        serializer = ComplaintSerializer(complaint)
        return Response(serializer.data, status=201)
    
    return Response(serializer.errors, status=400)




# ✅ Retrieve Single Complaint
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def complaint_detail(request, complaint_id):
    """
    Retrieve a complaint.
    - Admins can access all complaints.
    - Users can only access their own.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    if not request.user.is_admin and complaint.user != request.user:
        return Response({"error": "You can only view your own complaints"}, status=403)
    serializer = ComplaintSerializer(complaint)
    return Response(serializer.data)

# ✅ Update Complaint
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def complaint_update(request, complaint_id):
    """
    Update complaint.
    - Only Admins can update complaint details.
    - If status changes, it logs a status update.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    if not request.user.is_admin:
        return Response({"error": "Only admins can update complaint status"}, status=403)
    serializer = ComplaintSerializer(complaint, data=request.data, partial=True)
    
    if serializer.is_valid():
        old_status = complaint.status
        complaint = serializer.save()
        if 'status' in request.data and complaint.status != old_status:
            message = request.data.get('message', 'Status updated')
            StatusLog.objects.create(complaint=complaint, status=complaint.status, message=message)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# ✅ Delete Complaint
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def complaint_delete(request, complaint_id):
    """
    Delete a complaint.
    - Users can delete only their own complaints.
    - Admins can delete any complaint.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)
    if complaint.user != request.user and not request.user.is_admin:
        return Response({"error": "You can only delete your own complaints"}, status=403)
    complaint.delete()
    return Response({"message": "Complaint deleted successfully"}, status=200)
