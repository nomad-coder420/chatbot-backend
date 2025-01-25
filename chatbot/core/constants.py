from decouple import config

SYNC_DATABASE_URL = config("SYNC_DATABASE_URL")
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID", default="")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET", default="")
GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI_FE", default="")

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
