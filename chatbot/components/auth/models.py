from chatbot.core.models import BaseModel
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Authentication(BaseModel):
    __tablename__ = "auth_authentication"

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("user_user.id"),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    google_user_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    google_refresh_token: Mapped[str] = mapped_column(String, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="authentication")
