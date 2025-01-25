from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from chatbot.api.v1.request_response import (
    GetChatHistoryRequestSchema,
    GetChatHistoryResponseSchema,
    GoogleLoginRequestSchema,
    GoogleLoginResponseSchema,
    AskQueryRequestSchema,
    AskQueryResponseSchema,
)
from chatbot.api.v1.request_response import ErrorSchema
from chatbot.core.utils import get_db, get_user_id
from chatbot.flows.ask_query import AskQueryFlow
from chatbot.flows.get_chat_history import GetChatHistoryFlow
from chatbot.flows.get_user import GetUserFlow
from chatbot.flows.google_login import GoogleLoginFlow

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


@api_router.post(
    "/chat/ask_query",
    response_model=AskQueryResponseSchema,
    responses={400: {"model": ErrorSchema}, 500: {"model": ErrorSchema}},
)
def ask_query(
    validated_data: AskQueryRequestSchema,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id),
):
    query = validated_data.query

    user = GetUserFlow(db).execute_flow(user_id)
    response = AskQueryFlow(user, db).execute_flow(query)

    return response


@api_router.post(
    "/chat/get_history",
    response_model=GetChatHistoryResponseSchema,
    responses={400: {"model": ErrorSchema}, 500: {"model": ErrorSchema}},
)
def get_chat_history(
    validated_data: GetChatHistoryRequestSchema,
    db: Session = Depends(get_db),
    user_id: UUID = Depends(get_user_id),
):
    last_query_id = validated_data.last_query_id

    user = GetUserFlow(db).execute_flow(user_id)
    response = GetChatHistoryFlow(user, db).execute_flow(last_query_id)

    return response
