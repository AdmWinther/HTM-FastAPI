from fastapi import FastAPI
from uuid import uuid4
from Controller.UserController import UserRouter as userRouter
from Controller.LoginController import LoginController as loginRouter
from Controller.SecurityMiddleware import SecurityMiddleware
from Controller.VersionController import VersionRouter as versionRouter
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello My World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name} {uuid4()}"}


# app.add_middleware(CSRFMiddleware, allow_origin="*", allow_methods=["*"], allow_headers=["*"])
app.add_middleware(SecurityMiddleware)
app.include_router(userRouter, prefix="/api/user")
app.include_router(versionRouter, prefix="/version")
app.include_router(loginRouter, prefix="/login")