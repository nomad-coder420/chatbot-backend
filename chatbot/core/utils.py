import base64
from starlette.requests import Request


def get_db(request: Request):
    return request.state.db


def decode_base64url(base64url_str):
    padding = "=" * (4 - len(base64url_str) % 4)  # Add padding if necessary
    return base64.urlsafe_b64decode(base64url_str + padding)
