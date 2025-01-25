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
