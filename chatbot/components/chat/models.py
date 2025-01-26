from datetime import datetime
from uuid import uuid4, UUID as UUIDType
from sqlalchemy import (
    JSON,
    UUID,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from chatbot.components.chat.enums import QueryResponseStatus
from chatbot.core.models import BaseModel
from chatbot.components.user.models import User


class UserQuery(BaseModel):
    __tablename__ = "chat_userquery"

    query_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user_user.id"), nullable=False, index=True
    )
    query: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    meta: Mapped[dict] = mapped_column(JSON, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="queries")
    responses: Mapped["QueryResponse"] = relationship(
        "QueryResponse", back_populates="query"
    )


class QueryResponse(BaseModel):
    __tablename__ = "chat_queryresponse"

    response_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False
    )
    query_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chat_userquery.id"), nullable=False, index=True
    )
    response: Mapped[str] = mapped_column(String, nullable=False)
    response_status: Mapped[QueryResponseStatus] = mapped_column(
        Enum(QueryResponseStatus), default=QueryResponseStatus.CREATED, nullable=False
    )
    response_requested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    response_started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    response_completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    response_failed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    failure_reason: Mapped[dict] = mapped_column(
        JSON, server_default=func.json("{}"), nullable=False
    )

    query = relationship("UserQuery", back_populates="responses")
