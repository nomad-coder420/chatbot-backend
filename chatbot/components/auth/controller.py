from datetime import timedelta
from uuid import UUID
from chatbot.clients.jwt import JwtClient
from chatbot.components.auth.crud import AuthCrud
from chatbot.core.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)


class AuthController(AuthCrud):
    def create_refresh_token(self, user_id: UUID) -> str:
        refresh_token = JwtClient().create_token(
            data={"user_id": str(user_id)},
            expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return refresh_token

    def create_access_token(self, user_id: UUID) -> str:
        access_token = JwtClient().create_token(
            data={"user_id": str(user_id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        return access_token
