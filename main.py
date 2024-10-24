from sys import prefix
from uuid import uuid4

from fastapi import FastAPI
from typing import List
from uuid import uuid4
from Model.Entity.User import User
from Controller.UserController import router as userRouter
from Controller.loginController import router as loginRouter
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello My World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} {uuid4()}"}


app.include_router(userRouter, prefix="/api/user")
app.include_router(loginRouter, prefix="/login")