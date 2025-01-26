from uuid import UUID
from langchain.schema import HumanMessage, AIMessage
from langchain_core.runnables.config import RunnableConfig

from chatbot.components.chat.schemas import ChatSchema
from chatbot.llm_agent.agent import LlmAgent
from langchain.callbacks.base import BaseCallbackHandler, AsyncCallbackHandler


class LlmAgentController:
    def format_chat_history(
        self, chat_history: list[ChatSchema]
    ) -> list[HumanMessage | AIMessage]:
        formatted_chat_history: list[HumanMessage | AIMessage] = []

        for chat in chat_history[::-1]:
            query = chat.get("query") or ""
            response = chat.get("response") or ""

            formatted_chat_history.append(HumanMessage(content=query))
            if response:
                formatted_chat_history.append(AIMessage(content=response))

        return formatted_chat_history

    async def process_query(
        self,
        query: str,
        query_id: UUID,
        response_id: UUID,
        chat_history: list[ChatSchema],
    ):
        llm_agent = LlmAgent().get_agent()
        formatted_chat_history = self.format_chat_history(chat_history)

        initial_state = {
            "query": query,
            "query_id": query_id,
            "response_id": response_id,
            "chat_history": formatted_chat_history,
        }

        async for chunk in llm_agent.astream_events(
            initial_state,
            version="v2",
            config=RunnableConfig(callbacks=[AsyncCallbackHandler()]),
        ):
            event = chunk["event"]
            name = chunk["name"]

            if event == "on_custom_event" and name == "on_chunk_stream":
                data = chunk["data"]

                direct_stream_llm_response = data.get("direct_stream_llm_response")
                if direct_stream_llm_response:
                    yield data.get("chunk")
