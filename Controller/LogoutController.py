import os
from http.client import responses
from tabnanny import verbose

from fastapi import APIRouter, Form, Response
from starlette.responses import JSONResponse
from Model.Entity.User import User
from Service.CSRFService import CSRFService
from Service.UserService import UserService
from passlib.context import CryptContext
from Controller.JWTtoken import  create_access_token

LogoutRouter = APIRouter()

@LogoutRouter.post("")
async def logout(request: Response):
    verbose: bool = os.getenv("VERBOSE") == "True"
    deleteCSRFToken = await CSRFService.deleteCSRFToken(request=request)
    if(verbose):
        print(f"CSRF token deleted: {deleteCSRFToken}")

    response: Response = Response()
    #Set the CSRF token in the response header
    #CSRF token must never be stored in the cookie
    # response.headers["csrf_token"] = csrfToken
    response.set_cookie("jwt_token", "", httponly=True)

    return response