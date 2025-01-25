import base64
import jwt
from datetime import datetime, timedelta, timezone
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPublicNumbers
from cryptography.hazmat.backends import default_backend

from chatbot.core.constants import JWT_TOKEN_SECRET, JWT_TOKEN_ALGORITHM


def decode_base64url(base64url_str):
    padding = "=" * (4 - len(base64url_str) % 4)
    return base64.urlsafe_b64decode(base64url_str + padding)


class JwtClient:
    def create_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
        secret: str = "",
        algorithm: str | None = None,
    ) -> str:
        if not secret:
            secret = JWT_TOKEN_SECRET

        if not algorithm:
            algorithm = JWT_TOKEN_ALGORITHM

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
            to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, secret, algorithm=algorithm)

        return encoded_jwt

    def decode_token(
        self,
        jwt_token: str,
        secret: RSAPublicKey | str = "",
        algorithms: list[str] | None = None,
        audience: str | None = None,
    ) -> dict:
        if not secret:
            secret = JWT_TOKEN_SECRET

        if not algorithms:
            algorithms = [JWT_TOKEN_ALGORITHM]

        payload = jwt.decode(
            jwt_token, secret, algorithms=algorithms, audience=audience
        )
        return payload

    def get_unverified_header(self, jwt_token: str) -> dict:
        jwt_header = jwt.get_unverified_header(jwt_token)
        return jwt_header

    def is_token_expired(self, jwt_token: str) -> bool:
        payload = self.decode_token(jwt_token)

        expiry = payload.get("exp")

        if not expiry:
            return True

        expiry_datetime = datetime.fromtimestamp(expiry, tz=timezone.utc)

        return expiry_datetime < datetime.now(timezone.utc)

    def get_rsa_public_key(
        self, jwt_header: dict, public_keys: list[dict]
    ) -> RSAPublicKey:
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

        public_numbers = RSAPublicNumbers(n=n, e=e)

        rsa_public_key = public_numbers.public_key(default_backend())

        return rsa_public_key
