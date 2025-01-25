import json
from json import JSONEncoder
import requests

from chatbot.core.constants import (
    GOOGLE_PUBLIC_KEYS_URL,
    GOOGLE_PUBLIC_KEYS_VAR,
    GOOGLE_TOKEN_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
)


class GoogleClient:
    def get_token_data(self, code):
        payload = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        response = requests.post(
            GOOGLE_TOKEN_URL,
            data=json.dumps(payload, cls=JSONEncoder),
        )

        if response.status_code == 200:
            return response.json()

        print("Failed to get token data", response.status_code, response.text)
        raise Exception("Failed to get token data")

    def get_public_keys(self):
        global GOOGLE_PUBLIC_KEYS_VAR

        if GOOGLE_PUBLIC_KEYS_VAR:
            return GOOGLE_PUBLIC_KEYS_VAR

        response = requests.get(GOOGLE_PUBLIC_KEYS_URL)

        if response.status_code == 200:
            public_keys = response.json()

            GOOGLE_PUBLIC_KEYS_VAR = public_keys
            return public_keys

        print("Failed to get public keys", response.status_code, response.text)
        raise Exception("Failed to get public keys")
