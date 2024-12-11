from fastapi import Request
import utility.JWTtoken as JWTtoken

def GetUserIdFromRequest(request: Request):
    token: str = JWTtoken.getJwtTokenFromRequest(request)
    tokenPayload = JWTtoken.getTokenPayload(token)
    return tokenPayload["id"]