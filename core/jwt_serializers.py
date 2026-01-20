from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to authenticate using roll_no
    instead of default username.
    """
    username_field = "roll_no"

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
 # ✅ ADD CUSTOM CLAIMS
        token["roll_no"] = user.roll_no
        token["is_admin"] = user.is_admin

        return token
