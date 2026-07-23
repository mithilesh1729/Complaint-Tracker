from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.core.cache import cache

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that checks Redis to see if the token's JTI
    has been blacklisted (logged out).
    """
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)
        
        jti = validated_token.get('jti')
        if not jti:
            return validated_token

        # Check if this specific token ID is in our Redis Cache
        is_blacklisted = cache.get(f"blacklisted_token_{jti}")
        if is_blacklisted:
            raise AuthenticationFailed(
                "This token has been logged out/blacklisted.",
                code="token_not_valid"
            )
            
        return validated_token
