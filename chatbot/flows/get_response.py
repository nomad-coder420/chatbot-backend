import json
from uuid import UUID
from sqlalchemy.orm import Session

from chatbot.components.chat.crud import ChatCrud
from chatbot.components.chat.enums import QueryResponseStatus
from chatbot.components.user.models import User
from chatbot.llm_agent.agent import LlmAgent


class GetResponseFlow:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

        self.chat_controller = ChatCrud(self.user, self.db)

    async def get_llm_response(
        self, query, query_id, response_id, chat_history, response_obj
    ):
        llm_agent = LlmAgent().get_agent()
        initial_state = {
            "query": query,
            "query_id": query_id,
            "response_id": response_id,
            "chat_history": chat_history,
        }

        self.chat_controller.update_response_status(
            response_obj, QueryResponseStatus.IN_PROGRESS
        )

        response = ""
        async for chunk in llm_agent.astream_events(
            initial_state,
            version="v2",
        ):
            event = chunk["event"]
            name = chunk["name"]

            if event == "on_llm_stream":
                content = chunk["data"]["chunk"].text
                response += content

                yield f"data: {json.dumps(content)}\n\n"

            elif event == "on_chain_end":
                if name == "LangGraph":
                    yield "data: <end>\n\n"

        self.chat_controller.update_query_response(response_obj, response)
        self.chat_controller.update_response_status(
            response_obj, QueryResponseStatus.SUCCEEDED
        )

    def execute_flow(self, query_id: UUID):
        try:
            latest_query_obj = self.chat_controller.get_latest_query()

            if not latest_query_obj:
                raise Exception("User query not found")

            if latest_query_obj.query_id != query_id:
                raise Exception("Query id does not match")

            response_obj = self.chat_controller.create_query_response(
                query_id=latest_query_obj.id, response=""
            )

            chat_history, _ = self.chat_controller.get_chat_history(
                last_query_id=latest_query_obj.query_id
            )

            response = self.get_llm_response(
                latest_query_obj.query,
                latest_query_obj.query_id,
                response_obj.response_id,
                chat_history,
                response_obj,
            )

            headers = {"response_id": str(response_obj.response_id)}

            return response, headers
        except Exception as e:
            print(f"Error executing Get Response Flow: {e}")
            raise e
