import secrets
import string
from django.utils import timezone


from django.db import transaction

from core.models import (
    User,
    Hostel,
    Department,
    HostelAssignment,
)


class StudentService:
    """
    Business logic for Student Management.
    """

    @staticmethod
    def generate_temporary_password(length=10):
        alphabet = (
            string.ascii_letters
            + string.digits
            + "@#$%&!"
        )

        return "".join(
            secrets.choice(alphabet)
            for _ in range(length)
        )

    @staticmethod
    @transaction.atomic
    def create_student(
        *,
        roll_no,
        name,
        email,
        phone_number,
        department,
        hostel,
        room_no,
    ):
        """
        Creates a student along with hostel assignment.
        """

        temp_password = StudentService.generate_temporary_password()

        user = User.objects.create_user(
            roll_no=roll_no,
            email=email,
            password=temp_password,
            name=name,
            phone_number=phone_number,
            department=department,
            hostel=hostel.name,
            room_no=room_no,
            role="student",
            must_change_password=True,
        )

        HostelAssignment.objects.create(
            user=user,
            hostel=hostel,
            room_no=room_no,
            from_date=timezone.now().date(),
            is_current=True,
        )

        return user, temp_password
    
    
    
    @staticmethod
    @transaction.atomic
    def update_student(
        *,
        user,
        name,
        email,
        phone_number,
        department,
    ):

        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.department = department

        user.save()

        return user
    
    
    
    @staticmethod
    @transaction.atomic
    def transfer_hostel(
        *,
        user,
        hostel,
        room_no,
    ):

        current_assignment = (
            HostelAssignment.objects.filter(
                user=user,
                is_current=True,
            ).first()
        )

        if current_assignment:

            current_assignment.is_current = False
            current_assignment.to_date = timezone.now().date()

            current_assignment.save(
                update_fields=[
                    "is_current",
                    "to_date",
                ]
            )

        HostelAssignment.objects.create(
            user=user,
            hostel=hostel,
            room_no=room_no,
            from_date=timezone.now().date(),
            is_current=True,
        )

        user.hostel = hostel.name
        user.room_no = room_no

        user.save(
            update_fields=[
                "hostel",
                "room_no",
            ]
        )

        return user
    
    
    
    @staticmethod
    def deactivate_student(user):
        
        user.is_active = False

        user.save(
            update_fields=[
                "is_active",
            ]
        )

        return user
    
    @staticmethod
    def reset_password(user):

        temp_password = (
            StudentService.generate_temporary_password()
        )

        user.set_password(temp_password)

        user.must_change_password = True

        user.save(
            update_fields=[
                "password",
                "must_change_password",
            ]
        )

        return temp_password