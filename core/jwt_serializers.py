from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RollNoTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer to authenticate using roll_no
    instead of default username.
    """
    username_field = "roll_no"
