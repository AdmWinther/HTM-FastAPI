
from http.client import HTTPException
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from Controller.JWTtoken import verifyToken
from Controller.MyCORSMiddleware import MyCORSMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.method == "OPTIONS":
            # Respond to preflight requests with the appropriate CORS headers and status code 200
            headers: dict = MyCORSMiddleware.return_headers()
            print("I am sending a 200 response to an option request")
            return JSONResponse(content={"detail": "Options"}, status_code=200, headers=headers)

        # Control if the request needs authentication
        #The endpoints that start with /api are protected
        if "/api" not in request.url.path:
            #The endpoints that does not start with /api are unprotected and can be responded anyway.
            print("the endpoint is unprotected")

        else:
            #If the endpoint path include /api, it is protected and a valid token
            # must be provided in the request header
            if "Authorization" not in request.headers:
                print("the endpoint is protected but no token is provided")
                # Return error 401
                return JSONResponse({"detail":"no authentication token in the request."}, status_code=401)
            else:
                #Control if the token is valid
                token = request.headers["Authorization"]
                print(f"the endpoint is protected and token is provided by user is: {token}")

                isTokenValid = verifyToken(token)
                if isTokenValid == "":
                    message = "Access to a protected Endpoint authorized with a valid token"
                    print(message)

                else:
                    message = "Access to a protected Endpoint rejected due to an invalid token"
                    print(message)
                    return JSONResponse({"detail": f"{message}."}, status_code=401)

        print("now it is time to call the next middleware or call the endpoint")
        response = await call_next(request)
        return response