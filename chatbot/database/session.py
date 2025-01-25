from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from typing import Final, Optional
from contextvars import ContextVar, Token


from chatbot.core.constants import SYNC_DATABASE_URL

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(
    REQUEST_ID_CTX_KEY, default=None
)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()


def set_request_id(request_id: str) -> Token[Optional[str]]:
    return _request_id_ctx_var.set(request_id)


def reset_request_id(ctx_token: Token) -> None:
    return _request_id_ctx_var.reset(ctx_token)


sync_engine = create_engine(SYNC_DATABASE_URL, echo=False)
ScopedSessionLocal = scoped_session(
    sessionmaker(bind=sync_engine), scopefunc=get_request_id
)
