
from rest_framework import serializers
from core.models import Hostel,User
from core.services.staff_service import StaffService



class StaffSerializer(serializers.ModelSerializer):
    hostel = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.filter(is_active=True)
    )

    class Meta:
        model = User

        fields = [
            "roll_no",
            "name",
            "email",
            "phone_number",
            "hostel",
            "role",
            "is_active",
        ]

        read_only_fields = [
            "is_active",
        ]

    def create(self, validated_data):

        user, temp_password = StaffService.create_staff(
            roll_no=validated_data["roll_no"],
            name=validated_data["name"],
            email=validated_data["email"],
            phone_number=validated_data.get("phone_number", ""),
            hostel=validated_data["hostel"],
            role=validated_data["role"],
        )

        self.temp_password = temp_password

        return user
        
    def update(self, instance, validated_data):
        if "role" in validated_data:
            instance.role = validated_data.pop("role")
            
        hostel = validated_data.pop("hostel", None)
        if not hostel:
            hostel = Hostel.objects.get(name=instance.hostel) if instance.hostel else None
            
        instance = StaffService.update_staff(
            user=instance,
            name=validated_data.get("name", instance.name),
            email=validated_data.get("email", instance.email),
            phone_number=validated_data.get("phone_number", instance.phone_number),
            hostel=hostel,
        )
        
        if "role" in self.initial_data:
            instance.save(update_fields=["role"])
            
        return instance