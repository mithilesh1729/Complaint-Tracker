from rest_framework import serializers

from core.models import Complaint


class DashboardStatsSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    resolved = serializers.IntegerField()
    active = serializers.IntegerField()


class RecentComplaintSerializer(serializers.ModelSerializer):

    category = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Complaint

        fields = [
            "complaint_id",
            "complaint_number",
            "category",
            "status",
            "priority",
            "created_at",
        ]


class StudentDashboardSerializer(serializers.Serializer):

    stats = DashboardStatsSerializer()

    recent_complaints = RecentComplaintSerializer(
        many=True
    )