import os

from fastapi import FastAPI
from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware

from Controller.UserController import UserRouter
from Controller.LoginController import LoginRouter
from Controller.MySecurityMiddleware import MySecurityMiddleware
from Controller.VersionController import VersionRouter
from Controller.MyCORSMiddleware import MyCORSMiddleware
from Controller.MyOptionMiddleware import MyOptionMiddleware
from Controller.OrganizationController import organizationRouter
from Controller.CSRFController import CsrfRouter
from Controller.MyCSRFMiddleware import MyCSRFMiddleware
from Controller.LogoutController import LogoutRouter
app = FastAPI()

# Enable CORS



app.add_middleware(MyCSRFMiddleware)
app.add_middleware(MySecurityMiddleware)
app.add_middleware(MyOptionMiddleware)
app.add_middleware(MyCORSMiddleware)
app.include_router(UserRouter, prefix="/api/user")
app.include_router(VersionRouter, prefix="/version")
app.include_router(LoginRouter, prefix="/login")
app.include_router(organizationRouter, prefix="/api/organization")
app.include_router(CsrfRouter, prefix="/api/csrf")

app.include_router(LogoutRouter, prefix="/logout")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[f"{os.getenv("FRONTEND_URL")}"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


