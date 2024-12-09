from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from utility import JWTtoken
from Service.CSRFService import CSRFService

CsrfRouter = APIRouter()

@CsrfRouter.get("/")
async def makeNewCsrfToken(request: Request):
    if (request.cookies.get("jwt_token") == None):
        return JSONResponse({"error": "Unauthorized."}, status_code=401)
    else:
        if JWTtoken.verifyToken(request.cookies.get("jwt_token")) == False:
            return JSONResponse({"error": "Unauthorized."}, status_code=401)
        token = request.cookies.get("jwt_token")
        payload = JWTtoken.getTokenPayload(token)
        userId = payload['id']
        newCsrfToken = await CSRFService.getCsrfToken(userId)
        return JSONResponse({"csrf_token": newCsrfToken})
        # return  newCsrfToken