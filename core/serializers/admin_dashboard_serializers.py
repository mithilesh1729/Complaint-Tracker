from rest_framework import serializers

class AdminDashboardSerializer(serializers.Serializer):
    """
    Serializer for the Admin dashboard summary.
    """
    stats = serializers.DictField()
