
import os

from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
VersionRouter = APIRouter()

@VersionRouter.get("")
async def getVersion():
    # print("get-version-Start")
    # Include the CSRF token in the response headers
    csrf_token = "your_generated_csrf_token"
    headers: dict ={"x-xsrf-token" : csrf_token} #,
                    # "Access-Control-Allow-Origin": f"{os.getenv('FRONTEND_URL')}"}

    # Return a response with the CSRF token in the headers
    reply: dict = {"version": os.getenv("VERSION")}
    # print("get-version-End")
    return JSONResponse(content=reply, headers=headers)



@VersionRouter.post("")
async def postVersion():
    # print("post-version-start")
    csrf_token = "your_generated_csrf_token"
    # Include the CSRF token in the response headers
    headers: dict ={"x-xsrf-token" : csrf_token ,
                    "Access-Control-Allow-Origin": f"{os.getenv('FRONTEND_URL')}"}

    # Return a response with the CSRF token in the headers
    reply: dict = {"version": f"post{os.getenv("VERSION")}"}
    # print("post-version-End")
    return JSONResponse(content=reply, headers=headers)
