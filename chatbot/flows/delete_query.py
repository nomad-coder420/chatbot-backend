from uuid import UUID
from sqlalchemy.orm import Session

from chatbot.components.chat.crud import ChatCrud
from chatbot.components.user.models import User


class DeleteQueryFlow:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

        self.chat_controller = ChatCrud(self.user, self.db)

    def execute_flow(self, query_id: UUID):
        try:
            query_obj = self.chat_controller.get_user_query(query_id)

            if not query_obj:
                raise Exception("Query not found")

            self.chat_controller.delete_user_queries(query_obj.id)
            return {}
        except Exception as e:
            print(f"Error executing Delete Query Flow: {e}")
            raise e
