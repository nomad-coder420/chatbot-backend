from sqlalchemy.orm import Session

from chatbot.components.chat.crud import ChatCrud
from chatbot.components.user.models import User


class AskQueryFlow:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

        self.chat_controller = ChatCrud(self.user, self.db)

    def execute_flow(self, query: str):
        try:
            query_obj = self.chat_controller.create_user_query(query)
            response_obj = self.chat_controller.create_query_response(
                query_obj.id, "I don't know anything..."
            )

            return {
                "query_id": query_obj.query_id,
                "response_id": response_obj.response_id,
                "status": response_obj.response_status,
            }
        except Exception as e:
            print(f"Error executing Ask Query Flow: {e}")
            raise e
