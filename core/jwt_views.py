from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_serializers import RollNoTokenObtainPairSerializer

class RollNoTokenObtainPairView(TokenObtainPairView):
    """
    JWT login view that accepts roll_no + password
    """
    serializer_class = RollNoTokenObtainPairSerializer
