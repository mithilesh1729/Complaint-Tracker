from rest_framework import serializers

from core.models import Complaint
from core.models import ComplaintCategory

from core.utils.time import humanize_datetime


class ComplaintCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory

        fields = [
            "id",
            "name",
        ]


class ComplaintListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for complaint listing pages.
    """

    student_name = serializers.CharField(
        source="user.name",
        read_only=True,
    )

    category = ComplaintCategoryListSerializer(
        read_only=True,
    )

    assigned_to_name = serializers.CharField(
        source="assigned_to.name",
        read_only=True,
        allow_null=True,
    )

    created_at_human = serializers.SerializerMethodField()

    class Meta:
        model = Complaint

        fields = [
            "complaint_id",
            "complaint_number",
            "student_name",
            "hostel",
            "category",
            "priority",
            "status",
            "assigned_to_name",
            "created_at",
            "created_at_human",
            "is_confirmed",
        ]

    def get_created_at_human(self, obj):
        return humanize_datetime(obj.created_at)