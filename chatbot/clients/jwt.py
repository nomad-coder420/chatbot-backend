import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from datetime import datetime, timedelta, timezone


from chatbot.core.constants import JWT_TOKEN_SECRET, JWT_TOKEN_ALGORITHM


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
