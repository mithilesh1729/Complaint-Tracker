from django.db.models import Q
from django.shortcuts import get_object_or_404

from core.models import User, UserRole

class StudentSelector:

    @staticmethod
    def list_students(
        *,
        search=None,
        department=None,
        hostel=None,
        is_active=True,
    ):
        queryset = (
            User.objects
            .filter(role=UserRole.STUDENT, is_superuser=False, is_admin=False)
            .select_related("department")
            .order_by("roll_no")
        )

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active
            )

        if department:
            queryset = queryset.filter(
                department__code=department
            )

        if hostel:
            queryset = queryset.filter(
                hostel=hostel
            )

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                |
                Q(roll_no__icontains=search)
            )

        return queryset

    @staticmethod
    def get_student_or_404(roll_no):
        return get_object_or_404(
            User.objects.select_related("department"),
            roll_no=roll_no,
            role=UserRole.STUDENT,
        )    