from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from chatbot.components.user.crud import UserCrud


class GetUserFlow:
    def __init__(self, db: Session):
        self.db = db
        self.user_controller = UserCrud(self.db)

    def execute_flow(self, user_id: UUID):
        try:
            user_obj = self.user_controller.get_user_obj(user_id)

            if not user_obj:
                raise HTTPException(status_code=498, detail="Invalid user id")

            return user_obj
        except Exception as e:
            print(f"Error executing Get User Flow: {e}")
            raise e
