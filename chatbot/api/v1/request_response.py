from typing import Any

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    detail: Any
