from rest_framework import serializers
from .models import User, Complaint, ComplaintImage, StatusLog , Department , Hostel
from django.db import transaction
from core.services.student_service import StudentService

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['roll_no', 'name', 'hostel', 'room_no', 'email']

# Complaint Image Serializer
class ComplaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintImage
        fields = ['image', 'uploaded_at']


# Status Log Serializer
class StatusLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLog
        fields = ['status', 'message', 'timestamp']


# Complaint Serializer
class ComplaintSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ComplaintImageSerializer(many=True, read_only=True)

    # derived fields
    latest_admin_remark = serializers.SerializerMethodField()
    status_history = serializers.SerializerMethodField()

    class Meta:
        model = Complaint
        fields = [
            'complaint_id',

            # Core fields
            'complaint_type',
            'status',
            'created_at',
            'resolved_at',

            #  CONFIRMATION STATE 
            'is_confirmed',
            'confirmed_at',
            'student_feedback',

            # User-facing
            'user',
            'latest_admin_remark',

            # Detail fields
            'name',
            'hostel',
            'room_no',
            'phone_number',
            'priority',
            'description',
            'images',

            # Audit
            'status_history',
            'updated_at',
            
        ]

        read_only_fields = [
            'complaint_id',
            'created_at',
            'updated_at',
            'resolved_at',
            'status_history',
            'latest_admin_remark',
            'is_confirmed',
            'confirmed_at',
        ]

    
    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES.getlist('images')

        with transaction.atomic():
            complaint = Complaint.objects.create(
                user=request.user,
                name=validated_data.get('name', request.user.name),
                hostel=validated_data.get('hostel', request.user.hostel),
                room_no=validated_data['room_no'],
                phone_number=validated_data['phone_number'],
                complaint_type=validated_data['complaint_type'],
                description=validated_data['description'],
                priority=validated_data.get('priority', 'medium'),
            )

            for image in images_data:
                ComplaintImage.objects.create(
                    complaint=complaint,
                    image=image
                )

            return complaint


   
    # Latest Admin Remark
    def get_latest_admin_remark(self, obj):
        latest_log = (
            StatusLog.objects
            .filter(complaint=obj)
            .order_by('-timestamp')
            .first()
        )
        return latest_log.message if latest_log else None

  
    # Full Status History
    def get_status_history(self, obj):
        logs = StatusLog.objects.filter(complaint=obj).order_by('timestamp')
        return StatusLogSerializer(logs, many=True).data





class StudentCreateSerializer(serializers.Serializer):
    roll_no = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)

    email = serializers.EmailField()

    phone_number = serializers.CharField(
        max_length=15,
        required=False,
        allow_blank=True,
    )

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True)
    )

    hostel = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.filter(is_active=True)
    )

    room_no = serializers.CharField(
        max_length=10
    )

    def create(self, validated_data):
        user, password = StudentService.create_student(
            **validated_data
        )

        # attach password so the view can return it once
        user.temporary_password = password

        return user





class StudentListSerializer(serializers.ModelSerializer):

    department = serializers.CharField(
        source="department.code",
        read_only=True,
    )

    class Meta:
        model = User

        fields = (
            "roll_no",
            "name",
            "email",
            "phone_number",
            "department",
            "hostel",
            "room_no",
            "is_active",
        )



class StudentUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.filter(is_active=True),
        required=False,
    )

    hostel = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.filter(is_active=True),
        required=False,
    )

    room_no = serializers.CharField(required=False)



# ┌─────────────────────────────────────────────────────────────┐
# │                BACKEND (Django REST Framework)              │
# ├─────────────────────────────────────────────────────────────┤
# │  URLs (urls.py)                                             │
# │  ├─ /api/token/ → JWT login                                 │
# │  ├─ /api/complaints/ → List/Create                          │
# │  ├─ /api/complaints/<id>/ → Detail/Update/Delete            │
# │  ├─ /api/complaints/<id>/logs/ → Status history             │
# │  ├─ /api/complaints/<id>/slip/ → PDF download               │
# │  └─ /api/complaints/<id>/confirm/ → Student confirmation    │
# └─────────────────────┬───────────────────────────────────────┘
#                       │
#         ┌─────────────┴─────────────┐
#         │                           │
#    Views Layer                 Auth & Permissions
#    ──────────────              ──────────────────
#    views.py                    authentication.py
#    ├─ ComplaintListView        ├─ CsrfExemptSessionAuth
#    │  (CBV: filters,           └─ Skip CSRF for API
#    │   pagination, cache)
#    ├─ complaint_create         jwt_serializers.py
#    │  (FBV: file upload)       ├─ CustomTokenObtainSerializer
#    ├─ complaint_detail         │  (roll_no auth, custom claims)
#    ├─ complaint_update         jwt_views.py
#    ├─ complaint_delete         ├─ CustomTokenObtainPairView
#    ├─ complaint_logs           permissions.py
#    ├─ download_complaint_slip  ├─ IsOwnerOrAdmin
#    └─ confirm_complaint_resolution
#                                 (Object-level access)

#         ┌─────────────┴─────────────┐
#         │                           │
#    Serialization Layer         Utilities
#    ────────────────────         ──────────
#    serializers.py               pagination.py
#    ├─ ComplaintSerializer       ├─ CustomPagination (10/page)
#    │  (nested, derived fields)  throttling.py
#    ├─ UserSerializer            ├─ ComplaintRateThrottle (100/min)
#    ├─ ComplaintImageSerializer  signals.py
#    └─ StatusLogSerializer       ├─ pre_save: log status changes

#         ┌─────────────┴─────────────┐
#         │                           │
#    Models Layer                Configuration
#    ──────────────              ──────────────
#    models.py                    settings/base.py
#    ├─ User (roll_no PK)         ├─ DRF config, JWT settings
#    ├─ Complaint (UUID ID)       settings/dev.py
#    ├─ ComplaintImage             ├─ MySQL DB, CORS
#    └─ StatusLog

#         ┌─────────────┴─────────────┐
#         │                           │
#    Database Layer              Services
#    ──────────────              ──────────
#    MySQL                        services/pdf_service.py
#    ├─ Indexes on status,        ├─ Generate PDF slips
#    │  created_at                 └─ QR codes for confirmation
#    └─ Foreign keys, constraints