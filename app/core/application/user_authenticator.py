from core.domain.entities import UserContext


class UserAuthenticator:
    def __init__(self, jwt_service):
        self.jwt_service = jwt_service

    def authenticate(self, token: str):
        user_data = self.jwt_service.decode_token(token)
        return UserContext(
            guid=user_data["guid"],
            email=user_data["email"],
            roles=[]#user_data.get("roles", [])
        )
