from rest_framework import serializers
from .models import User, Complaint, ComplaintImage, StatusLog

# ✅ User Serializer (For Read & Write Operations)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['roll_no', 'hostel', 'room_no', 'email']

# ✅ Complaint Image Serializer (For Handling Multiple Images)
class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image', 'uploaded_at']

# ✅ Complaint Serializer (Nested User & Image Support)
class ComplaintSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # 🎯 Nested User Info (Read-Only)
    images = ComplaintImageSerializer(many=True, read_only=True)  # 🎯 Nested Images (Read-Only)
    
    class Meta:
        model = Complaint
        fields = ['complaint_id', 'user', 'complaint_type', 'description', 'images', 'status', 'priority', 'created_at', 'updated_at']

    # ✅ Custom `create` method for supporting multiple image uploads
    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES.getlist('images')  # 🎯 Multiple images handle karne ke liye
        complaint = Complaint.objects.create(**validated_data)
        
        for image in images_data:
            ComplaintImage.objects.create(complaint=complaint, image=image)
        
        return complaint

# ✅ Status Log Serializer (For Status History)
class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = ['status', 'message', 'timestamp']
