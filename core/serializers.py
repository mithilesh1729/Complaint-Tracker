from rest_framework import serializers
from .models import User, Complaint, ComplaintImage, StatusLog

# ✅ User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['roll_no', 'name', 'hostel', 'room_no', 'email']

# ✅ Complaint Image Serializer
class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image', 'uploaded_at']

# ✅ Complaint Serializer
class ComplaintSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ComplaintImageSerializer(many=True, read_only=True)

    class Meta:
        model = Complaint
        fields = ['complaint_id', 'user', 'name', 'hostel', 'room_no', 'phone_number', 
                  'complaint_type', 'description', 'images', 'status', 'priority', 
                  'created_at', 'updated_at', 'resolved_at']  # Added resolved_at

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES.getlist('images')
        complaint = Complaint.objects.create(
            user=request.user,
            name=validated_data['name'],
            hostel=validated_data['hostel'],
            room_no=validated_data['room_no'],
            phone_number=validated_data['phone_number'],
            complaint_type=validated_data['complaint_type'],
            description=validated_data['description'],
        )
        for image in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image)
        return complaint

# ✅ Status Log Serializer
class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = ['status', 'message', 'timestamp']