from fastapi import APIRouter, Form
from Model.Entity.User import User
from Service.UserService import UserService
from passlib.context import CryptContext
from Controller.JWTtoken import  create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)
LoginController = APIRouter()


@LoginController.post("")
async def login(username: str = Form(...), password: str = Form(...)):
    # print("login is reached.")
    # print(f"username is {username}")
    # print(f"password is {password}")
    fetchUser = await UserService.getUserByEmail(username)
    if len(fetchUser) == 0:
        return "Bad credential."
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
        return jwtToken
    else:
        return "Bad credential."