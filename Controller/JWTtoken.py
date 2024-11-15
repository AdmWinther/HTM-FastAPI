import os
from datetime import datetime

import jwt
from datetime import datetime, timedelta

from fastapi import HTTPException


def create_access_token(data: dict):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    expires_delta = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")))
    print("expires_delta")
    print(expires_delta)

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyToken(token: str):
    # print("VerifyToken()")
    # print(f"token is {token}")
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        if jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) is not None:
            tokenRenewal: bool = isTokenAboutToExpire(token)

            tokenValid: bool = True

            return tokenValid, tokenRenewal
            # return True
    except jwt.ExpiredSignatureError:
        print(f"token is expired {token}")
        return "token is expired"
    except jwt.InvalidTokenError:
        print("token is invalid")
        return "token is invalid"
    except Exception as e:
        print(f"Exception: {e}")
        return f"error {e}"

def getTokenPayload(token: str):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"payload is {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        print("the token is expired")
        return "the token is expired"
    except jwt.InvalidTokenError:
        print("the token is invalid")
        return "the token is invalid"
    except Exception as e:
        return f"error {e}"

def renewToken(token: str):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return create_access_token(data=payload)
    except jwt.ExpiredSignatureError:
        print("Token Renew failed, the token is expired")
        return "the token is expired"
    except jwt.InvalidTokenError:
        print("Token Renew failed, the token is invalid")
        return "the token is invalid"
    except Exception as e:
        print("Token Renew failed, an error occurred")
        return f"error {e}"

def isTokenAboutToExpire(token: str):
    tokenPayload: dict = getTokenPayload(token)
    # print(f"tokenPayload is {tokenPayload}")
    tokenRenewLimit = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_LIMIT")))
    untilExpire = datetime.fromtimestamp(tokenPayload["exp"]) - datetime.now() + timedelta(hours=float(os.getenv("LOCAL2UTC_TIME_DIFFERENCE")))

    print(f"untilExpire: {untilExpire}")
    if untilExpire < tokenRenewLimit:
        print("Token is about to expire")
        return True
    else:
        print("Token is not about to expire")
        return False