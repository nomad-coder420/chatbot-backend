from sqlalchemy.orm import Session
from chatbot.components.auth.models import Authentication
from chatbot.components.user.models import User


class AuthCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_auth_obj(self, google_user_id: str) -> Authentication | None:
        return (
            self.db.query(Authentication)
            .filter(Authentication.google_user_id == google_user_id)
            .first()
        )

    def create_auth_obj(
        self,
        user_obj: User,
        google_user_id: str,
        google_refresh_token: str,
        refresh_token: str,
    ):
        auth_obj = Authentication(
            user_id=user_obj.id,
            google_user_id=google_user_id,
            google_refresh_token=google_refresh_token,
            refresh_token=refresh_token,
        )

        self.db.add(auth_obj)
        self.db.flush()
        self.db.refresh(auth_obj)

        return auth_obj

    def update_auth_obj(self, auth_obj: Authentication, refresh_token: str):
        auth_obj = self.db.merge(auth_obj)

        auth_obj.refresh_token = refresh_token

        self.db.flush()
        self.db.refresh(auth_obj)

        return auth_obj
