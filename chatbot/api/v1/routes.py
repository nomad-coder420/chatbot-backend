from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chatbot.api.v1.auth.request_response import (
    GoogleLoginRequestSchema,
    GoogleLoginResponseSchema,
)
from chatbot.api.v1.request_response import ErrorSchema
from chatbot.core.utils import get_db
from chatbot.flows.google_login_flow import GoogleLoginFlow

api_router = APIRouter()


@api_router.post(
    "/auth/google/login",
    response_model=GoogleLoginResponseSchema,
    responses={400: {"model": ErrorSchema}, 500: {"model": ErrorSchema}},
)
def login(validated_data: GoogleLoginRequestSchema, db: Session = Depends(get_db)):
    code = validated_data.code

    response = GoogleLoginFlow(db).execute_flow(code)

    return response
