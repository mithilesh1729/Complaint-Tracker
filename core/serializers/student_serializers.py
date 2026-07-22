from rest_framework import serializers
from core.models import User,Department,Hostel

from core.services.student_service import StudentService


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

    def validate_email(self, value):
        if not value.endswith("@nitp.ac.in"):
            raise serializers.ValidationError("Email must end with @nitp.ac.in")
        return value

    def validate_roll_no(self, value):
        if User.objects.filter(roll_no=value).exists():
            raise serializers.ValidationError(f"User with Roll No {value} already exists.")
        return value

    def validate_phone_number(self, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

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
    
    
    
    
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]