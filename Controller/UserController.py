from typing import List
from fastapi import APIRouter
from starlette.responses import JSONResponse

from Service.UserService import UserService
from Model.Entity.User import User

UserRouter = APIRouter()


@UserRouter.get("")
async def getAllUsers():
    return await UserService.getAllUsers()

@UserRouter.post("")
async def post_user(userInfo : dict):
    userInfo["password"] = User.get_password_hash(userInfo["password"])
    userInfo["emailAddress"] = userInfo["emailAddress"].lower()
    user: User = User(**userInfo)
    try:
        return await UserService.addUser(user)
        # return db
    except ValueError as e:
        return {"error": str(e)}

@UserRouter.get("/reset")
async def resetDatabase():
    print("resetting database")
    return await UserService.resetDatabase()

@UserRouter.get("/id/{userId}")
async def getUserById(userId: str):
    print(f"userid in controller: {userId}")
    return await UserService.getUserById(userId)

@UserRouter.get("/email/{emailAddress}")
async def getUserByEmail(emailAddress: str):
    return await UserService.getUserByEmail(emailAddress)

@UserRouter.get("/userType")
async def getUserType():
    print("UserType-get in controller")
    data: dict = {"value": "ADMIN"}
    return (data)