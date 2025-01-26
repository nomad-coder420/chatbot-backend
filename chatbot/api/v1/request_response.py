from typing import Any
from uuid import UUID

from pydantic import BaseModel

from chatbot.components.chat.enums import QueryResponseStatus


class ErrorSchema(BaseModel):
    detail: Any


class GoogleLoginRequestSchema(BaseModel):
    code: str


class GoogleLoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str


class AskQueryRequestSchema(BaseModel):
    query: str


class AskQueryResponseSchema(BaseModel):
    query_id: UUID


class GetChatHistoryRequestSchema(BaseModel):
    last_query_id: UUID | None


class GetChatHistoryResponseSchema(BaseModel):
    chat_history: list
    is_last_page: bool


class DeletrQueryRequestSchema(BaseModel):
    query_id: UUID


class DeletrQueryResponseSchema(BaseModel):
    pass
