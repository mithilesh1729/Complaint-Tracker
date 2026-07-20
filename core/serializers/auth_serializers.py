from rest_framework import serializers
from core.serializers.student_serializers import DepartmentSerializer
from core.models import User


class ProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "roll_no",
            "name",
            "email",
            "phone_number",
            "role",
            "is_admin",
            "hostel",
            "room_no",
            "department",
            "is_active",
        ]
        
    def get_role(self, obj):
        if obj.is_staff or obj.is_superuser or obj.is_admin:
            return "admin"
        return obj.role
        