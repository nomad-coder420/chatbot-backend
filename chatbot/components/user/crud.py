from uuid import UUID
from chatbot.components.user.models import User


class UserCrud:
    def __init__(self, db):
        self.db = db

    def create_user_obj(self, name: str, email: str) -> User:
        user_obj = User(name=name, email=email)

        self.db.add(user_obj)
        self.db.flush()
        self.db.refresh(user_obj)

        return user_obj

    def get_user_obj(self, user_id: UUID) -> User:
        user_obj = self.db.query(User).filter(User.user_id == user_id).first()
        return user_obj
