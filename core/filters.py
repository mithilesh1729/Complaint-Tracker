import django_filters

from core.models import Complaint


class ComplaintFilter(django_filters.FilterSet):
    priority = django_filters.CharFilter()

    status = django_filters.CharFilter()

    category = django_filters.NumberFilter(
        field_name="category_id",
    )

    assigned_to = django_filters.UUIDFilter(
        field_name="assigned_to_id",
    )

    class Meta:
        model = Complaint

        fields = [
            "priority",
            "status",
            "category",
            "assigned_to",
        ]