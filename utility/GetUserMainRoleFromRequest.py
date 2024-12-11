from fastapi import Request
import utility.JWTtoken as JWTtoken

def GetUserMainRoleFromRequest(request: Request):
    token: str = JWTtoken.getJwtTokenFromRequest(request)
    tokenPayload = JWTtoken.getTokenPayload(token)
    userRoles = tokenPayload["role"]
    return userRoles[0]