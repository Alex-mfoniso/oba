import os

from django.contrib.auth import authenticate, get_user_model
from rest_framework.authentication import BaseAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class ApiKeyAuthentication(BaseAuthentication):
    header_name = "HTTP_X_API_KEY"

    def authenticate(self, request):
        api_key = request.META.get(self.header_name)
        if not api_key:
            return None

        expected_api_key = os.getenv("API_KEY", "")
        if not expected_api_key or api_key != expected_api_key:
            raise AuthenticationFailed("Invalid API key.")

        user = self._resolve_user()
        return (user, api_key)

    def _resolve_user(self):
        user_model = get_user_model()
        username = os.getenv("API_KEY_USER", "")
        if username:
            user = user_model.objects.filter(username=username).first()
            if user:
                return user

        user = user_model.objects.filter(is_active=True).order_by("id").first()
        if user:
            return user

        return user_model.objects.create_user(username="api-key-user", password=os.getenv("API_KEY_USER_PASSWORD", "ChangeMe123!"))


def issue_bearer_token(user):
    token, _ = Token.objects.get_or_create(user=user)
    return token.key


def authenticate_user(username, password):
    return authenticate(username=username, password=password)
