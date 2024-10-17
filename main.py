from uuid import uuid4

from fastapi import FastAPI
from typing import List
from uuid import uuid4
from Model.Entity.User import User
from Controller.User import router as user_router

app = FastAPI()

db: List[User] = [
    User(
        name="Robert",
        lastName="Adam",
        emailAddress="peter@yes.com",
        password="password"
    ),
    User(
        name="John",
        lastName="Doe",
        emailAddress="jamal@tabrixi.com",
        password="password"),
    User(
        name="Jeanny",
        lastName="Karman",
        emailAddress="Jane@Carman.com",
        password="password")
]

@app.get("/")
async def root():
    return {"message": "Hello My World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} {uuid4()}"}


@app.get("/api/user")
async def get_user():
    return db

@app.post("/api/user")
async def get_user(user : User):
    try:
        db.append(user)
        return db
    except ValueError as e:
        return {"error": str(e)}

app.include_router(user_router, prefix="/api/user")