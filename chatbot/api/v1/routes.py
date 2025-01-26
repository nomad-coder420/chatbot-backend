from uuid import UUID
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from chatbot.api.v1.request_response import (
    DeletrQueryRequestSchema,
    DeletrQueryResponseSchema,
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
from chatbot.flows.delete_query import DeleteQueryFlow
from chatbot.flows.get_chat_history import GetChatHistoryFlow
from chatbot.flows.get_response import GetResponseFlow
from chatbot.flows.get_user import GetUserFlow
from chatbot.flows.google_login import GoogleLoginFlow

api_router = APIRouter()


@api_router.post(
    "/auth/google/login",
    response_model=GoogleLoginResponseSchema,
    responses={
        400: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
def login(validated_data: GoogleLoginRequestSchema, db: Session = Depends(get_db)):
    code = validated_data.code

    response = GoogleLoginFlow(db).execute_flow(code)

    return response


@api_router.post(
    "/chat/get_history",
    response_model=GetChatHistoryResponseSchema,
    responses={
        400: {"model": ErrorSchema},
        498: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
def get_chat_history(
    validated_data: GetChatHistoryRequestSchema,
    user_id: UUID = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    last_query_id = validated_data.last_query_id

    user = GetUserFlow(db).execute_flow(user_id)
    response = GetChatHistoryFlow(user, db).execute_flow(last_query_id)

    return response


@api_router.post(
    "/chat/ask_query",
    response_model=AskQueryResponseSchema,
    responses={
        400: {"model": ErrorSchema},
        498: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
def ask_query(
    validated_data: AskQueryRequestSchema,
    user_id: UUID = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    query = validated_data.query

    user = GetUserFlow(db).execute_flow(user_id)
    response = AskQueryFlow(user, db).execute_flow(query)

    return response


@api_router.get("/chat/get_response")
def get_response(
    request: Request,
    query_id: UUID,
    user_id: UUID = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    if not query_id:
        raise Exception("No query id provided")

    user = GetUserFlow(db).execute_flow(user_id)
    response, headers = GetResponseFlow(user, db).execute_flow(query_id)

    return StreamingResponse(response, media_type="text/event-stream", headers=headers)


@api_router.post(
    "/chat/delete_query",
    response_model=DeletrQueryResponseSchema,
    responses={
        400: {"model": ErrorSchema},
        498: {"model": ErrorSchema},
        500: {"model": ErrorSchema},
    },
)
def delete_query(
    validated_data: DeletrQueryRequestSchema,
    user_id: UUID = Depends(get_user_id),
    db: Session = Depends(get_db),
):
    query_id = validated_data.query_id

    user = GetUserFlow(db).execute_flow(user_id)
    response = DeleteQueryFlow(user, db).execute_flow(query_id)

    return response
