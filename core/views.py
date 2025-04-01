from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Complaint, StatusLog
from .serializers import ComplaintSerializer
from django.contrib.auth import get_user_model

# Get the custom User model (if using a custom user model instead of Django's default)
User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Ensure only authenticated users can access
def complaint_list(request):
    """
    Retrieve a list of complaints.
    - Admin users can view all complaints.
    - Regular users can only see their own complaints.
    """
    if getattr(request.user, 'is_admin', False):  # Ensure 'is_admin' exists in the user model
        complaints = Complaint.objects.all()
    else:
        complaints = Complaint.objects.filter(user=request.user)  # Filter complaints for the logged-in user
    serializer = ComplaintSerializer(complaints, many=True)  # Serialize the queryset
    return Response(serializer.data)  # Return serialized data as JSON response

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Only authenticated users can create complaints
def complaint_create(request):
    """
    Create a new complaint.

    - Regular users can submit their own complaints.
    - Admin users can create complaints on behalf of students using their 'roll_no'.
    """
    serializer = ComplaintSerializer(data=request.data, context={'request': request})  # Deserialize request data
    if serializer.is_valid():
        user = request.user  # Default to the logged-in user
        # If admin is creating a complaint for a student using roll_no
        if getattr(request.user, 'is_admin', False) and 'roll_no' in request.data:
            try:
                user = User.objects.get(roll_no=request.data['roll_no'])  # Get user by roll_no
            except User.DoesNotExist:
                return Response({"error": "Invalid roll number"}, status=400)  # Return error if user not found
        serializer.save(user=user)  # Save the complaint with the determined user
        return Response(serializer.data, status=201)  # Return created complaint data
    return Response(serializer.errors, status=400)  # Return validation errors if invalid data is provided

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # Only authenticated users can view complaint details
def complaint_detail(request, complaint_id):
    """
    Retrieve details of a specific complaint.
    
    - Admin users can view any complaint.
    - Regular users can only view their own complaints.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)  # Retrieve complaint or return 404
    # Restrict non-admin users from accessing other users' complaints
    if not getattr(request.user, 'is_admin', False) and complaint.user != request.user:
        return Response({"error": "Unauthorized"}, status=403)  # Forbidden response for unauthorized access
    serializer = ComplaintSerializer(complaint)  # Serialize the complaint object
    return Response(serializer.data)  # Return serialized complaint details

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])  # Only authenticated users can update complaints
def complaint_update(request, complaint_id):
    """
    Update complaint details (only for admins).
    
    - Only admins can update the complaint status.
    - If the status changes, a log entry is created.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)  # Retrieve complaint or return 404
    # Restrict updates to admins only
    if not getattr(request.user, 'is_admin', False):
        return Response({"error": "Only admins can update complaint status"}, status=403)  # Forbidden response
    serializer = ComplaintSerializer(complaint, data=request.data, partial=True)  # Partial update
    if serializer.is_valid():
        old_status = complaint.status  # Store previous status before updating
        complaint = serializer.save()  # Save updated complaint
        # Log status change if it was updated
        if 'status' in request.data and complaint.status != old_status:
            message = request.data.get('message', 'Status updated')  # Default message if none provided
            StatusLog.objects.create(complaint=complaint, status=complaint.status, message=message)  # Log status update
        return Response(serializer.data)  # Return updated complaint data
    return Response(serializer.errors, status=400)  # Return validation errors

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])  # Only authenticated users can delete complaints
def complaint_delete(request, complaint_id):
    """
    Delete a complaint.
    
    - Regular users can delete only their own complaints.
    - Admin users can delete any complaint.
    """
    complaint = get_object_or_404(Complaint, complaint_id=complaint_id)  # Retrieve complaint or return 404
    # Only allow deletion if the user owns the complaint or is an admin
    if complaint.user != request.user and not getattr(request.user, 'is_admin', False):
        return Response({"error": "Unauthorized"}, status=403)  # Forbidden response for unauthorized access
    complaint.delete()  # Delete the complaint from the database
    return Response({"message": "Complaint deleted successfully"}, status=200)  # Return success message
