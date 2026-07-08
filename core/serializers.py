from rest_framework import serializers
from .models import User, Complaint, ComplaintImage, StatusLog , Department , Hostel
from django.db import transaction
from core.services.student_service import StudentService

from core.services.complaint_service import ComplaintService
from core.models import ComplaintCategory
from core.services.staff_service import StaffService

# # User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['roll_no', 'name', 'hostel', 'room_no', 'email'] 


# class DepartmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Department
#         fields = ["id", "name"]
        
        
# class ProfileSerializer(serializers.ModelSerializer):
#     department = DepartmentSerializer(read_only=True)

#     class Meta:
#         model = User
#         fields = [
#             "roll_no",
#             "name",
#             "email",
#             "phone_number",
#             "role",
#             "hostel",
#             "room_no",
#             "department",
#             "is_active",
#         ]
        
        

# # Complaint Image Serializer
# class ComplaintImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComplaintImage
#         fields = ['image', 'uploaded_at']
        

# class ComplaintCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ComplaintCategory
#         fields = [
#             "id",
#             "name",
#             "description",
#         ]        


# # Status Log Serializer
# class StatusLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StatusLog
#         fields = ['status', 'message', 'timestamp']


# class ComplaintSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     images = ComplaintImageSerializer(many=True, read_only=True)

#     # New fields
#     category = ComplaintCategorySerializer(read_only=True)
    
#     category_id = serializers.PrimaryKeyRelatedField(
#         queryset=ComplaintCategory.objects.filter(
#             is_active=True
#         ),
#         source="category",
#         write_only=True,
#     )

#     location_details = serializers.CharField(
#         required=False,
#         allow_blank=True,
#     )

#     # Derived fields
#     latest_admin_remark = serializers.SerializerMethodField()
#     status_history = serializers.SerializerMethodField()

#     class Meta:
#         model = Complaint

#         fields = [
#             "complaint_id",

#             # Complaint
#             "category",
#             "category_id",
#             "description",
#             "location_details",
#             "priority",
#             "status",

#             # Dates
#             "created_at",
#             "updated_at",
#             "resolved_at",

#             # Student confirmation
#             "is_confirmed",
#             "confirmed_at",
#             "student_feedback",

#             # Relations
#             "user",
#             "images",

#             # Derived
#             "latest_admin_remark",
#             "status_history",
#         ]

#         read_only_fields = [
#             "complaint_id",
#             "created_at",
#             "updated_at",
#             "resolved_at",
#             "latest_admin_remark",
#             "status_history",
#             "is_confirmed",
#             "confirmed_at",
#         ]

#     def create(self, validated_data):

#         request = self.context["request"]

#         images = request.FILES.getlist("images")

#         complaint = ComplaintService.create_complaint(
#             user=request.user,
#             category=validated_data["category"],
#             description=validated_data["description"],
#             location_details=validated_data.get(
#                 "location_details",
#                 "",
#             ),
#             priority=validated_data.get(
#                 "priority",
#                 "medium",
#             ),
#         )

#         for image in images:
#             ComplaintImage.objects.create(
#                 complaint=complaint,
#                 image=image,
#             )

#         return complaint

#     def get_latest_admin_remark(self, obj):
#         latest_log = (
#             StatusLog.objects
#             .filter(complaint=obj)
#             .order_by("-timestamp")
#             .first()
#         )

#         return latest_log.message if latest_log else None

#     def get_status_history(self, obj):
#         logs = (
#             StatusLog.objects
#             .filter(complaint=obj)
#             .order_by("timestamp")
#         )

#         return StatusLogSerializer(
#             logs,
#             many=True,
#         ).data




# class StudentCreateSerializer(serializers.Serializer):
#     roll_no = serializers.CharField(max_length=20)
#     name = serializers.CharField(max_length=100)

#     email = serializers.EmailField()

#     phone_number = serializers.CharField(
#         max_length=15,
#         required=False,
#         allow_blank=True,
#     )

#     department = serializers.PrimaryKeyRelatedField(
#         queryset=Department.objects.filter(is_active=True)
#     )

#     hostel = serializers.PrimaryKeyRelatedField(
#         queryset=Hostel.objects.filter(is_active=True)
#     )

#     room_no = serializers.CharField(
#         max_length=10
#     )

#     def create(self, validated_data):
#         user, password = StudentService.create_student(
#             **validated_data
#         )

#         # attach password so the view can return it once
#         user.temporary_password = password

#         return user





# class StudentListSerializer(serializers.ModelSerializer):

#     department = serializers.CharField(
#         source="department.code",
#         read_only=True,
#     )

#     class Meta:
#         model = User

#         fields = (
#             "roll_no",
#             "name",
#             "email",
#             "phone_number",
#             "department",
#             "hostel",
#             "room_no",
#             "is_active",
#         )



# class StudentUpdateSerializer(serializers.Serializer):
#     name = serializers.CharField(required=False)
#     email = serializers.EmailField(required=False)
#     phone_number = serializers.CharField(required=False)

#     department = serializers.PrimaryKeyRelatedField(
#         queryset=Department.objects.filter(is_active=True),
#         required=False,
#     )

#     hostel = serializers.PrimaryKeyRelatedField(
#         queryset=Hostel.objects.filter(is_active=True),
#         required=False,
#     )

#     room_no = serializers.CharField(required=False)
