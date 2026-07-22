from django.db import transaction

from core.models import User
from core.services.user_service import UserService
from core.tasks import send_credentials_email_task

class StaffService:
    """
    Business logic for Staff Management.
    """

    @staticmethod
    @transaction.atomic
    def create_staff(
        *,
        roll_no,
        name,
        email,
        phone_number,
        hostel,
        role,
    ):
        temp_password = UserService.generate_temporary_password()

        user = User.objects.create_user(
            roll_no=roll_no,
            email=email,
            password=temp_password,
            name=name,
            phone_number=phone_number,
            hostel=hostel.name,
            role=role,
            must_change_password=True,
        )

        send_credentials_email_task.delay(user.email, user.name, temp_password, is_reset=False)

        return user, temp_password

    @staticmethod
    def reset_password(user):
        user, temp_password = UserService.reset_password(user)
        send_credentials_email_task.delay(user.email, user.name, temp_password, is_reset=True)
        return user, temp_password

    @staticmethod
    @transaction.atomic
    def update_staff(
        *,
        user,
        name,
        email,
        phone_number,
        hostel,
    ):
        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.hostel = hostel.name

        user.save(
            update_fields=[
                "name",
                "email",
                "phone_number",
                "hostel",
            ]
        )

        return user