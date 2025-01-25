from uuid import UUID
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

from chatbot.clients.jwt import JwtClient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/google")


def get_user_id(token: str = Depends(oauth2_scheme)) -> UUID:
    payload = JwtClient().decode_token(token)
    user_id = payload.get("user_id", None)

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    return UUID(user_id)


def get_db(request: Request):
    return request.state.db
