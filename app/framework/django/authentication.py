from decouple import config
from rest_framework.authentication import BaseAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from core.application.user_authenticator import UserAuthenticator
from infraestructure.authentication.jwt_service import JwtService


from rest_framework.exceptions import AuthenticationFailed
import jwt

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
            print(payload["guid"])
            user = {"guid": payload["guid"], "email": payload["email"]}
            return (user, None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
