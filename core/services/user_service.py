import secrets
import string


class UserService:
    """
    Shared user account utilities.
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
    def reset_password(user):
        password = UserService.generate_temporary_password()

        user.set_password(password)
        user.must_change_password = True

        user.save(
            update_fields=[
                "password",
                "must_change_password",
            ]
        )

        return password

    @staticmethod
    def deactivate(user):
        user.is_active = False

        user.save(
            update_fields=[
                "is_active",
            ]
        )

        return user

    @staticmethod
    def activate(user):
        user.is_active = True

        user.save(
            update_fields=[
                "is_active",
            ]
        )

        return user