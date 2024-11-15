import os
from http.client import responses

from fastapi import APIRouter, Form, Response
from starlette.responses import JSONResponse
from Model.Entity.User import User
from Service.UserService import UserService
from passlib.context import CryptContext
from Controller.JWTtoken import  create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    # print(plain_password, hashed_password)
    # print(f"result of comparing the plain password with hash password: {pwd_context.verify(plain_password, hashed_password)}")
    return pwd_context.verify(plain_password, hashed_password)
LoginController = APIRouter()


@LoginController.post("")
async def login(username: str = Form(...), password: str = Form(...)):

    fetchUser = await UserService.getUserByEmail(username)
    if len(fetchUser) == 0:
        return JSONResponse(content = {"detail": "Username not found."}, status_code=401)
    hashedPass = User.get_password_hash(password)
    if verify_password(password, fetchUser[0]["password"]):
        data = {
            "sub": username,
            "role": "user",
            "id": fetchUser[0]["id"],
            "name": fetchUser[0]["name"],
            "lastName": fetchUser[0]["lastName"],
        }

        jwtToken = create_access_token(data=data)
        print(f"jwtToken generated at login: {jwtToken}")
        response: Response = Response()
        response.set_cookie("jwt_token", jwtToken, httponly=True)

        return response
    else:
        return JSONResponse({"detail": "Bad credential."}, status_code=401)