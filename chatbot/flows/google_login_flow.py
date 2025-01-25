from sqlalchemy.orm import Session
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


from chatbot.clients.google import GoogleClient
from chatbot.clients.jwt import JwtClient
from chatbot.components.auth.controller import AuthController
from chatbot.components.user.crud import UserCrud
from chatbot.core.constants import GOOGLE_CLIENT_ID
from chatbot.core.utils import decode_base64url


class GoogleLoginFlow:
    def __init__(self, db: Session):
        self.db = db

        self.jwt_client = JwtClient()
        self.auth_controller = AuthController(self.db)
        self.user_controller = UserCrud(self.db)

    def execute_flow(self, code: str):
        try:
            token_data = GoogleClient().get_token_data(code)

            id_token = token_data.get("id_token")
            jwt_header = self.jwt_client.get_unverified_header(id_token)

            google_public_keys = GoogleClient().get_public_keys()
            public_keys = google_public_keys.get("keys") or []

            jwt_public_key = None
            for key in public_keys:
                if key.get("kid") == jwt_header.get("kid"):
                    jwt_public_key = key

            if not jwt_public_key:
                raise Exception("Public key not found for 'kid' in JWT header.")

            n_bytes = decode_base64url(jwt_public_key["n"])
            e_bytes = decode_base64url(jwt_public_key["e"])

            n = int.from_bytes(n_bytes, byteorder="big")
            e = int.from_bytes(e_bytes, byteorder="big")

            public_numbers = rsa.RSAPublicNumbers(n=n, e=e)

            rsa_public_key = public_numbers.public_key(default_backend())

            user_info = self.jwt_client.decode_token(
                id_token, rsa_public_key, ["RS256"], GOOGLE_CLIENT_ID
            )

            google_user_id = user_info.get("sub")

            print("Google user info:", user_info)

            if not google_user_id:
                raise Exception("Google user id not found in user info.")

            auth_obj = self.auth_controller.get_auth_obj(google_user_id)
            user_obj = None
            refresh_token = None

            if auth_obj:
                user_obj = auth_obj.user
                refresh_token = auth_obj.refresh_token

                if self.jwt_client.is_token_expired(refresh_token):
                    refresh_token = self.auth_controller.create_refresh_token(
                        user_obj.user_id
                    )
                    self.auth_controller.update_auth_obj(auth_obj, refresh_token)

            else:
                user_name = user_info.get("name")
                user_email = user_info.get("email")

                if not user_name or not user_email:
                    raise Exception("User name or email not found in user info.")
                user_obj = self.user_controller.create_user_obj(
                    name=user_name, email=user_email
                )

                refresh_token = self.auth_controller.create_refresh_token(
                    user_obj.user_id
                )
                auth_obj = self.auth_controller.create_auth_obj(
                    user_obj,
                    google_user_id,
                    token_data.get("refresh_token"),
                    refresh_token,
                )

            if not refresh_token:
                raise Exception("Refresh token not found")

            access_token = self.auth_controller.create_access_token(user_obj.user_id)

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }
        except Exception as e:
            print(f"Error executing Google Login Flow: {e}")
            raise e
