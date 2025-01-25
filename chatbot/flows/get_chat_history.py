from uuid import UUID
from sqlalchemy.orm import Session

from chatbot.components.chat.crud import ChatCrud
from chatbot.components.user.models import User


class GetChatHistoryFlow:
    def __init__(self, user: User, db: Session):
        self.user = user
        self.db = db

        self.chat_controller = ChatCrud(self.user, self.db)

    def execute_flow(self, last_query_id: UUID | None = None):
        try:
            chat_history, is_last_page = self.chat_controller.get_chat_history(
                last_query_id=last_query_id
            )

            return {"chat_history": chat_history, "is_last_page": is_last_page}
        except Exception as e:
            print(f"Error fetching chat history: {e}")
            return []
