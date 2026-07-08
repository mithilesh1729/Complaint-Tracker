from rest_framework import serializers
from core.serializers.student_serializers import DepartmentSerializer
from core.models import User


class ProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "roll_no",
            "name",
            "email",
            "phone_number",
            "role",
            "hostel",
            "room_no",
            "department",
            "is_active",
        ]
        