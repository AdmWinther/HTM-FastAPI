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
async def postUser(userInfo : dict):
    try:
        return await UserService.addUserByDictWithValidation(userInfo)
        # return db
    except ValueError as e:
        return {"error": str(e)}

@UserRouter.get("/reset")
async def resetOnlyUserTable():
    print("resetting database")
    user: dict = {"name": "user", "lastName": "user", "emailAddress": "user@user.com", "password": "user"}
    admin: dict = {"name": "admin", "lastName": "admin", "emailAddress": "admin@admin.com", "password": "user"}
    try:
        await UserService.deleteAll()
        await postUser(user)
        await postUser(admin)
        return {"message": "Database reset"}
    except ValueError as e:
        return {"error": str(e)}

@UserRouter.get("/id/{userId}")
async def getUserById(userId: str):
    print(f"userid in controller: {userId}")
    return await UserService.getUserById(userId)

@UserRouter.get("/email/{emailAddress}")
async def getUserByEmail(emailAddress: str):
    return await UserService.getUserByEmail(emailAddress)

@UserRouter.get("/userRole")
async def getUserRole():
    print("UserType-get in controller")
    data: dict = {"roles": ["ADMIN"]}
    return (data)


async def getUserRoleByUserName(username: str):
    print("UserType-get in controller")
    data: dict = {"roles": ["ADMIN"]}
    return (data)

def addSuperUser(userId, organizationId):
    return UserService.addSuperUser(userId, organizationId)