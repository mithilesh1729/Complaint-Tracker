from rest_framework import serializers
from core.models import Complaint,ComplaintImage, ComplaintCategory,StatusLog,User

from core.services.complaint_service import ComplaintService



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['roll_no', 'name', 'hostel', 'room_no', 'email'] 


# Complaint Image Serializer
class ComplaintImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ComplaintImage
        fields = [
            "image",
            "uploaded_at",
        ]

    def get_image(self, obj):
        request = self.context.get("request")

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url
        

class ComplaintCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory
        fields = [
            "id",
            "name",
            "description",
            "display_order",
            "is_active",
        ]        


# Status Log Serializer
class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = ['status', 'message', 'timestamp']


class ComplaintSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ComplaintImageSerializer(many=True, read_only=True)

    # New fields
    category = ComplaintCategorySerializer(read_only=True)
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ComplaintCategory.objects.filter(
            is_active=True
        ),
        source="category",
        write_only=True,
    )

    location_details = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    # Derived fields
    latest_admin_remark = serializers.SerializerMethodField()
    status_history = serializers.SerializerMethodField()

    class Meta:
        model = Complaint

        fields = [
            "complaint_id",

            # Complaint
            "category",
            "complaint_number",
            "category_id",
            "description",
            "location_details",
            "priority",
            "status",

            # Dates
            "created_at",
            "updated_at",
            "resolved_at",

            # Student confirmation
            "is_confirmed",
            "confirmed_at",
            "student_feedback",

            # Relations
            "user",
            "images",

            # Derived
            "latest_admin_remark",
            "status_history",
        ]

        read_only_fields = [
            "complaint_id",
            "created_at",
            "updated_at",
            "resolved_at",
            "latest_admin_remark",
            "status_history",
            "is_confirmed",
            "confirmed_at",
        ]

    def create(self, validated_data):

        request = self.context["request"]

        images = request.FILES.getlist("images")

        complaint = ComplaintService.create_complaint(
            user=request.user,
            category=validated_data["category"],
            description=validated_data["description"],
            location_details=validated_data.get(
                "location_details",
                "",
            ),
            priority=validated_data.get(
                "priority",
                "medium",
            ),
        )

        for image in images:
            ComplaintImage.objects.create(
                complaint=complaint,
                image=image,
            )

        return complaint

    def get_latest_admin_remark(self, obj):
        # Prevent N+1 by using prefetched data
        logs = [log for log in obj.status_logs.all() if log.status in ["in_progress", "resolved"]]
        if logs:
            latest = sorted(logs, key=lambda x: x.timestamp, reverse=True)[0]
            return latest.message
        return None

    def get_status_history(self, obj):
        logs = sorted(obj.status_logs.all(), key=lambda x: x.timestamp)
        return StatusLogSerializer(logs, many=True).data
    def get_fields(self):
        """
        Pass serializer context (especially request)
        to nested serializers.
        """
        fields = super().get_fields()

        fields["images"].context.update(self.context)

        return fields    

        