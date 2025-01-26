from typing_extensions import TypedDict
from uuid import UUID

from chatbot.components.chat.enums import QueryResponseStatus


class ChatSchema(TypedDict):
    query: str
    response: str
    query_id: UUID
    response_id: UUID
    status: QueryResponseStatus
