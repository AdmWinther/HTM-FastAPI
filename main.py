import os

from fastapi import FastAPI
from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware

from Controller.UserController import UserRouter as userRouter
from Controller.LoginController import LoginController as loginRouter
from Controller.MySecurityMiddleware import MySecurityMiddleware
from Controller.VersionController import VersionRouter as versionRouter
from Controller.MyCORSMiddleware import MyCORSMiddleware
from Controller.MyOptionMiddleware import MyOptionMiddleware
from Controller.OrganizationController import organizationRouter
app = FastAPI()

# Enable CORS


# app.add_middleware(CSRFMiddleware, allow_origin="*", allow_methods=["*"], allow_headers=["*"])
app.add_middleware(MySecurityMiddleware)
app.add_middleware(MyOptionMiddleware)
app.add_middleware(MyCORSMiddleware)
app.include_router(userRouter, prefix="/api/user")
app.include_router(versionRouter, prefix="/version")
app.include_router(loginRouter, prefix="/login")
app.include_router(organizationRouter, prefix="/api/organization")


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[f"{os.getenv("FRONTEND_URL")}"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


