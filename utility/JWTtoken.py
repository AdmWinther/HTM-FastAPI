import os
from datetime import datetime

import jwt
from datetime import datetime, timedelta

from fastapi import Request


def create_access_token(data: dict):
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    expires_delta = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")))
    # print("expires_delta")
    # print(expires_delta)

    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verifyToken(token: str):
    verbose: bool = os.getenv("VERBOSE") == "True"

    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        if jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) is not None:
            tokenValid: bool = True
            return tokenValid
            # return True
    except jwt.ExpiredSignatureError:
        if verbose: print(f"Token verification FAILED, token is expired {token}")
        return False
    except jwt.InvalidTokenError:
        if verbose: ("Token verification FAILED, token is invalid")
        return False
    except Exception as e:
        if verbose: print(f"Exception: {e}")
        return f"error {e}"

def getTokenPayload(token: str):
    verbose: bool = os.getenv("VERBOSE") == "True"
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print(f"payload is {payload}")
        return payload
    except jwt.ExpiredSignatureError:
        if verbose: print("Cannot get the Token payload because the token is expired in getTokenPayload")
        return "the token is expired"
    except jwt.InvalidTokenError:
        if verbose: print("Cannot get the Token payload because the token is invalid in getTokenPayload")
        return "the token is invalid"
    except Exception as e:
        return f"error {e}"

def renewToken(token: str):
    verbose: bool = os.getenv("VERBOSE") == "True"
    SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    ALGORITHM = os.getenv("JWT_ALGORITHM")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return create_access_token(data=payload)
    except jwt.ExpiredSignatureError:
        if verbose: print("Token Renew failed, the token is expired")
        return "the token is expired"
    except jwt.InvalidTokenError:
        if verbose: print("Token Renew failed, the token is invalid")
        return "the token is invalid"
    except Exception as e:
        if verbose: print("Token Renew failed, an error occurred")
        return f"error {e}"

def isTokenAboutToExpire(token: str):
    verbose : bool = os.getenv("VERBOSE") == "True"
    tokenPayload: dict = getTokenPayload(token)
    if verbose: print(f"tokenPayload is {tokenPayload}")
    tokenRenewLimit = timedelta(minutes=float(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_LIMIT")))
    untilExpire = datetime.fromtimestamp(tokenPayload["exp"]) - datetime.now() + timedelta(hours=float(os.getenv("LOCAL2UTC_TIME_DIFFERENCE")))

    if verbose: print(f"untilExpire: {untilExpire}")
    if untilExpire < tokenRenewLimit:
        if verbose: print("Token is about to expire")
        return True
    else:
        if verbose: print("Token is not about to expire")
        return False

def getUsernameFromRequest(request: Request):
    token: str = getJwtTokenFromRequest(request)
    tokenPayload : dict = getTokenPayload(token)
    return tokenPayload["sub"]

def getUserIdFromRequest(request: Request):
    token: str = getJwtTokenFromRequest(request)
    tokenPayload : dict = getTokenPayload(token)
    return tokenPayload["id"]

def getAllCookiesFromRequestHeader(request: Request):
    verbose : bool = os.getenv("VERBOSE") == "True"
    splitCookies = request.headers["cookie"].split(";")
    allCookies = list(map(lambda cookie: cookie.split("="), splitCookies))
    allCookies = list(map(lambda cookie: (cookie[0].strip(), cookie[1].strip()), allCookies))
    if verbose: print(f"allCookies made in getAllCookiesFromRequestHeader are: {allCookies}")
    return allCookies

def getJwtTokenFromRequest(request: Request):
    verbose: bool = os.getenv("VERBOSE") == "True"
    allCookies = getAllCookiesFromRequestHeader(request)
    for cookie in allCookies:
        if cookie[0] == "jwt_token":
            return cookie[1]
    if verbose: print("No jwt_token found in the request header")
    return "Error, no jwt_token found in the request header"

def getCsrfTokenFromRequestHeader(request: Request):
    verbose: bool = os.getenv("VERBOSE") == "True"
    allCookies = getAllCookiesFromRequestHeader(request)
    for cookie in allCookies:
        if cookie[0] == "csrf_token":
            return cookie[1]
    if verbose: print("No csrf_token found in the request header")
    return "Error, no csrf_token found in the request header"

def getUserRoleFromJwtTokenPayload(JwtToken : str):
    verbose : bool = os.getenv("VERBOSE") == "True"
    tokenPayload = getTokenPayload(JwtToken)
    if verbose:
        print(f"about to get user role for {tokenPayload['sub']} from token payload.")
    userRole = tokenPayload["role"]
    if verbose:
        print(f"userRoleDict is fetched successfully: {userRole}")
    # The user might have multiple roles. The roles are stored in a list.
    return  userRole