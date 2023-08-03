from decouple import config
from pathlib import Path
from jose import jwt
from jose.constants import ALGORITHMS
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization

# Replace with your own values
SECRET_KEY = "your-secret-key"
ALGORITHM = "RS256"
PRIVATE_KEY_PATH = config("JWT_SECRET_KEY")
PUBLIC_KEY_PATH = config("JWT_PUBLIC_KEY")
TOKEN_EXPIRATION = timedelta(hours=1)


# def generate_token():
#     payload = {
#         "sub": "user_id",
#         "iat": datetime.utcnow(),
#         "exp": datetime.utcnow() + TOKEN_EXPIRATION,
#     }
#     token = jwt.encode(payload, PRIVATE_KEY_PATH, algorithm=ALGORITHM)
#     return {"token": token}
#
#
# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, PUBLIC_KEY_PATH, algorithms=[ALGORITHM])
#         return {"valid": True, "payload": payload}
#     except jwt.JWTError:
#         return {"valid": False}


if __name__ == "__main__":
    a = Path(__file__).parent.parent.parent.resolve()
    a = a.parent.parent.parent.joinpath("private_key.pem")
    print(a)
