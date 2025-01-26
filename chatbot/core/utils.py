from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from starlette.requests import Request

from chatbot.clients.jwt import JwtClient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/google")


def get_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    try:
        payload = JwtClient().decode_token(token)
        user_id = payload.get("user_id", None)

        if not user_id:
            raise HTTPException(status_code=498, detail="Invalid token")

        return UUID(user_id)
    except ExpiredSignatureError:
        raise HTTPException(status_code=498, detail="Token expired")


def get_db(request: Request):
    return request.state.db
