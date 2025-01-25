from uuid import uuid4, UUID as UUIDType
from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chatbot.core.models import BaseModel
from chatbot.components.auth.models import Authentication


class User(BaseModel):
    __tablename__ = "user_user"

    user_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    authentication: Mapped["Authentication"] = relationship(
        "Authentication", back_populates="user", uselist=False
    )
