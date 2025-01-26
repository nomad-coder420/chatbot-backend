from typing_extensions import TypedDict
from uuid import UUID

from chatbot.components.chat.schemas import ChatSchema


class AgentState(TypedDict):
    query: str
    response: str
    query_id: UUID
    response_id: UUID
    chat_history: list[ChatSchema]
    contextualised_query: str
    next_prompt_options: list[str]
