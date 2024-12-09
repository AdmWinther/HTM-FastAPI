import os

from fastapi import APIRouter, Response
from Service.CSRFService import CSRFService

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