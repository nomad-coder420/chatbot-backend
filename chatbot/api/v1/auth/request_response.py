from pydantic import BaseModel


class GoogleLoginRequestSchema(BaseModel):
    code: str


class GoogleLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
