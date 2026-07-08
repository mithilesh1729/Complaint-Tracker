from django.db.models import Q

from core.models import User


class StaffSelector:
    """
    Read-only queries for Staff Management.
    """

    @staticmethod
    def get_staff(roll_no):
        return User.objects.get(
            roll_no=roll_no,
        )

    @staticmethod
    def list_staff():

        return (
            User.objects.filter(
                role__in=[
                    "hostel_office",
                    "warden",
                    "hmc",
                ]
            )
            .select_related("department")
            .order_by("roll_no")
        )

    @staticmethod
    def search(queryset, search):

        if not search:
            return queryset

        return queryset.filter(
            Q(name__icontains=search)
            |
            Q(roll_no__icontains=search)
            |
            Q(email__icontains=search)
        )