
from http.client import HTTPException
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from Controller.JWTtoken import verifyToken



class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)


        protectedEndpoints = ["/api/user/id", "/api/organization"]
        # Control if the request needs authentication
        #control if the endpoint path includes /api it is not protected
        if "/api" not in request.url.path:
            print("the endpoint is unprotected")
            return response

        #If the endpoint path include /api, it is protected and a valid token
        # must be provided in the request header

        if "Authorization" not in request.headers:
            print("the endpoint is protected but no token is provided")
            # Return error 401
            return JSONResponse({"detail":"no authentication token in the request."}, status_code=401)
        else:
            print("the endpoint is protected and token is provided")
            #Control if the token is valid
            token = request.headers["Authorization"]
            print(f"token is {token}")
            isTokenValid = verifyToken(token)
            if isTokenValid == "":
                message = "Access to a protected Endpoint authorized with a valid token"
                print(message)
                return response
            else:

                message = "Access to a protected Endpoint rejected due to an invalid token"
                print(message)
                return JSONResponse({"detail": f"{message}."}, status_code=401)
