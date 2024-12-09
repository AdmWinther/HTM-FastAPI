import os

from fastapi import APIRouter, Form, Response
from starlette.responses import JSONResponse
from Service.S01_UserService import UserService
from passlib.context import CryptContext
from utility.JWTtoken import  create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    # print(plain_password, hashed_password)
    # print(f"result of comparing the plain password with hash password: {pwd_context.verify(plain_password, hashed_password)}")
    return pwd_context.verify(plain_password, hashed_password)
LoginRouter = APIRouter()


@LoginRouter.post("")
async def login(username: str = Form(...), password: str = Form(...)):
    fetchUser = await UserService.getUserByEmail(username)
    if len(fetchUser) == 0:
        return JSONResponse(content = {"error": "Username not found."}, status_code=401)

    if verify_password(password, fetchUser[0]["password"]):
        userRoles = await UserService.getUserRoleByUserId(fetchUser[0]["id"])
        print(f"User roles: {userRoles}")
        data = {
            "sub": username,
            "role": userRoles,
            "id": fetchUser[0]["id"],
            "name": fetchUser[0]["name"],
            "lastName": fetchUser[0]["lastName"]
        }

        jwtToken = create_access_token(data=data)
        print(f"jwtToken generated at login: {jwtToken}")

        # Generate CSRF token
        # csrfToken = await CSRFService.GenerateCSRFToken(data["id"])
        response: Response = JSONResponse({os.getenv("REACT_APP_LOCAL_STORAGE_USER_ROLES"): userRoles})
        #Set the CSRF token in the response header
        #CSRF token must never be stored in the cookie
        # response.headers["csrf_token"] = csrfToken
        response.set_cookie("jwt_token", jwtToken, httponly=True)

        return response
    else:
        return JSONResponse({"error": "Bad credential."}, status_code=401)