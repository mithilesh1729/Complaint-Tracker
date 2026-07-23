from rest_framework_simplejwt.views import TokenObtainPairView
from .jwt_serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            access_token_obj = request.auth
            
            # Blacklist the refresh token
            if refresh_token:
                token = RefreshToken(refresh_token)
                # TTL is remaining lifetime
                ttl = token.lifetime.total_seconds()
                cache.set(f"blacklisted_token_{token['jti']}", True, timeout=int(ttl))
                
            # Blacklist the access token
            if access_token_obj:
                ttl = access_token_obj.lifetime.total_seconds()
                cache.set(f"blacklisted_token_{access_token_obj['jti']}", True, timeout=int(ttl))

            return Response({"message": "Successfully logged out."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
