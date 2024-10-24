import os

import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException


def create_access_token(data: dict):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    expires_delta = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")))

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyToken(token: str):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"payload is {payload}")

        username: str = payload.get("sub")
        user_role: str = payload.get("role")
        return ""
    except jwt.ExpiredSignatureError:
        return "token is expired"
    except jwt.InvalidTokenError:
        return "token is invalid"
    except Exception as e:
        return f"error {e}"