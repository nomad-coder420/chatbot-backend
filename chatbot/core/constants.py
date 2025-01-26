import os
from decouple import config

SYNC_DATABASE_URL = config("SYNC_DATABASE_URL")
JWT_TOKEN_SECRET = config("JWT_TOKEN_SECRET")
JWT_TOKEN_ALGORITHM = config("JWT_TOKEN_ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES", default=60))
REFRESH_TOKEN_EXPIRE_DAYS = int(config("REFRESH_TOKEN_EXPIRE_DAYS", default=7))
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", default="")
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
HUGGINGFACEHUB_API_TOKEN = config("HUGGINGFACEHUB_API_TOKEN", default="")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_PUBLIC_KEYS_URL = "https://www.googleapis.com/oauth2/v3/certs"

GOOGLE_PUBLIC_KEYS_VAR: dict[str, list[dict]] = {}
