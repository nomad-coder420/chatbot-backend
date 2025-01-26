from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from chatbot.components.chat.schemas import ChatSchema
from chatbot.database.session import AsyncSessionLocal
from chatbot.components.chat.async_crud import AsyncChatCrud
from chatbot.components.chat.crud import ChatCrud
from chatbot.components.chat.enums import QueryResponseStatus
from chatbot.components.user.models import User
from chatbot.llm_agent.agent import LlmAgent
from chatbot.llm_agent.controller import LlmAgentController


class GetResponseFlow:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

        self.chat_controller = ChatCrud(self.user, self.db)
        self.llm_agent_controller = LlmAgentController()

    async def get_llm_response(
        self,
        query: str,
        query_id: UUID,
        response_id: UUID,
        chat_history: list[ChatSchema],
    ):
        async with AsyncSessionLocal() as async_db:
            async_chat_controller = AsyncChatCrud(async_db)

            try:
                response_obj = await async_chat_controller.get_response_obj(response_id)

                self.chat_controller.update_response_status(
                    response_obj, QueryResponseStatus.IN_PROGRESS
                )

                response = ""
                async for chunk in self.llm_agent_controller.process_query(
                    query, query_id, response_id, chat_history
                ):
                    response += chunk
                    yield chunk

                await async_chat_controller.update_query_response(
                    response_obj, response
                )
                await async_chat_controller.update_response_status(
                    response_obj, QueryResponseStatus.SUCCEEDED
                )
            except SQLAlchemyError as e:
                await async_db.rollback()

                try:
                    await async_chat_controller.update_response_failed(response_obj, e)
                except Exception as err:
                    print("Error updating response status:", err)

                raise e

            except Exception as e:
                await async_chat_controller.update_response_failed(response_obj, e)
                raise e

    def execute_flow(self, query_id: UUID):
        response_obj = None

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
            )

            headers = {"response_id": str(response_obj.response_id)}

            return response, headers
        except Exception as e:
            print(f"Error executing Get Response Flow: {e}")

            if response_obj:
                self.chat_controller.update_response_failed(response_obj, e)

            raise e
