from typing import List
from fastapi import APIRouter
from Service.UserService import UserService
from Model.Entity.User import User

router = APIRouter()


@router.get("")
async def getAllUsers():
    return await UserService.getAllUsers()

@router.post("")
async def post_user(userInfo : dict):
    userInfo["password"] = User.get_password_hash(userInfo["password"])
    userInfo["emailAddress"] = userInfo["emailAddress"].lower()
    user: User = User(**userInfo)
    try:
        return await UserService.addUser(user)
        # return db
    except ValueError as e:
        return {"error": str(e)}

@router.get("/reset")
async def resetDatabase():
    print("resetting database")
    return await UserService.resetDatabase()

@router.get("/id/{userId}")
async def getUserById(userId: str):
    print(f"userid in controller: {userId}")
    return await UserService.getUserById(userId)

@router.get("/email/{emailAddress}")
async def getUserByEmail(emailAddress: str):
    return await UserService.getUserByEmail(emailAddress)