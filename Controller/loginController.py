from fastapi import APIRouter, Form
from Model.Entity.User import User
from Service.UserService import UserService
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    print(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)
router = APIRouter()


@router.post("")
async def login(username: str = Form(...), password: str = Form(...)):
    print("login is reached.")
    # username = credentials["user"]
    # password = credentials["password"]
    print(f"username is {username}")
    print(f"password is {password}")
    hashedPass = User.get_password_hash(password)
    fetchUser = await UserService.getUserByEmail(username)
    if verify_password(password, fetchUser[0]["password"]):
        return "login soccessful."
    else:
        return "Bad credential."