from datetime import datetime

import jwt
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class JwtService:

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def decode_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            if datetime.fromtimestamp(payload["exp"]) < datetime.now():
                raise AuthenticationFailed("Token has expired")
            return payload
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")