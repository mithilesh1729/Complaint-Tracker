from django.utils.timesince import timesince
from django.utils.timezone import now

from rest_framework import serializers

from core.models import Complaint,ComplaintCategory



class DashboardCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplaintCategory

        fields = [
            "id",
            "name",
        ]

class OfficeDashboardComplaintSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for the Office Dashboard.
    """

    category = DashboardCategorySerializer(
            read_only=True,
    )

    student_name = serializers.CharField(source="user.name")

    created_at_human = serializers.SerializerMethodField()

    class Meta:
        model = Complaint

        fields = [
            "complaint_id",
            "complaint_number",
            "student_name",
            "category",
            "priority",
            "status",
            "created_at",
            "created_at_human",
        ]

    def get_created_at_human(self, obj):
        return f"{timesince(obj.created_at, now())} ago"


class OfficeDashboardSerializer(serializers.Serializer):
    """
    Serializer for the Hostel Office dashboard.
    """

    stats = serializers.DictField()

    recent_complaints = OfficeDashboardComplaintSerializer(
        many=True,
        read_only=True,
    )