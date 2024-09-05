from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import CustomUser


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        try:
            user = CustomUser.objects.get(token=token)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid token')
        if user.is_token_expired():
            raise AuthenticationFailed('Token has expired')
        return (user, None)
