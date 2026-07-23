
from rest_framework import serializers
from core.models import Hostel,User
from core.services.staff_service import StaffService



class StaffSerializer(serializers.ModelSerializer):
    hostel = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.filter(is_active=True),
        allow_null=True,
        required=False
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

    def validate_email(self, value):
        if not value.endswith("@nitp.ac.in"):
            raise serializers.ValidationError("Email must end with @nitp.ac.in")
        return value

    def validate_roll_no(self, value):
        # We only check duplicates on creation. StaffSerializer is a ModelSerializer 
        # so DRF automatically runs unique validators if the model field is unique.
        # But roll_no is the PrimaryKey! So let's manually enforce a better error message if needed.
        if self.instance is None and User.objects.filter(roll_no=value).exists():
            raise serializers.ValidationError(f"Staff with ID {value} already exists.")
        return value

    def validate_phone_number(self, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value

    def validate(self, data):
        role = data.get("role") or (self.instance.role if self.instance else None)
        hostel = data.get("hostel")
        
        # If updating and hostel isn't provided, check existing
        if self.instance and "hostel" not in data:
            hostel = Hostel.objects.get(name=self.instance.hostel) if self.instance.hostel else None

        if role in ["warden", "hostel_office"] and not hostel:
            raise serializers.ValidationError({"hostel": f"Hostel is required for {role}."})
            
        if role == "hmc":
            data["hostel"] = None
            
        return data

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