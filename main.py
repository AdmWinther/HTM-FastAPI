import os

from fastapi import FastAPI
from uuid import uuid4

from fastapi.middleware.cors import CORSMiddleware

from Controller.C01_UserController import UserRouter
from Controller.C50_LoginController import LoginRouter
from Controller.MW01_MySecurityMiddleware import MySecurityMiddleware
from Controller.C00_VersionController import VersionRouter
from Controller.MW02_MyCORSMiddleware import MyCORSMiddleware
from Controller.MW04_MyOptionMiddleware import MyOptionMiddleware
from Controller.C02_OrganizationController import organizationRouter
from Controller.C52_CSRFController import CsrfRouter
from Controller.MW03_MyCSRFMiddleware import MyCSRFMiddleware
from Controller.C51_LogoutController import LogoutRouter
from Controller.C03_ProjectController import projectRouter
app = FastAPI()

# Enable CORS



app.add_middleware(MyCSRFMiddleware)
app.add_middleware(MySecurityMiddleware)
app.add_middleware(MyOptionMiddleware)
app.add_middleware(MyCORSMiddleware)
app.include_router(VersionRouter, prefix="/version")
app.include_router(LoginRouter, prefix="/login")
app.include_router(UserRouter, prefix="/api/user")
app.include_router(organizationRouter, prefix="/api/organization")

app.include_router(projectRouter, prefix="/api/project")

app.include_router(CsrfRouter, prefix="/api/csrf")

app.include_router(LogoutRouter, prefix="/logout")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[f"{os.getenv("FRONTEND_URL")}"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


