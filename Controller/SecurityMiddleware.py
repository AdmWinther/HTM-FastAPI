import os

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from Controller import UserController
from Controller.JWTtoken import verifyToken, getTokenPayload, renewToken
from Controller.MyCORSMiddleware import MyCORSMiddleware
from Controller.EndpointAccess import access


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"SecurityMiddleware is called for {request.url.path}")
        # todo: Delete the following line after the development is completed
        temporaryUnprotectedEndpoints = ["/api/user/reset"]
        token = ""

        # the variable tokenRenew is used to control the token renewal.
        # If the token is about to be expired the tokenRenew is set to True when token is verified.
        # token will be renewed only if the token lifetime is less than the renewal time.
        tokenRenew: bool = False

        #************************************************************************************************
        #***********************************  request origin control  ***********************************
        #************************************************************************************************
        # Control the request origin, the request must come from the frontend domain.
        if "Origin" not in request.headers:
            print("No Origin in the request header")
            return JSONResponse({"detail": "Unauthorized."}, status_code=401)
        if request.headers["Origin"] != os.getenv("FRONTEND_URL"):
            print("Origin is not the frontend")
            return JSONResponse({"detail": "Unauthorized."}, status_code=401)

        #************************************************************************************************
        #*********************************  response to Option Request  *********************************
        #************************************************************************************************
        # Control the request origin, the request must come from the frontend domain.
        if request.method == "OPTIONS":
            # Respond to preflight requests with the appropriate CORS headers and status code 200
            headers: dict = MyCORSMiddleware.return_headers()
            print(f"I am sending a 200 response to an option request to {request.url.path}")
            return JSONResponse(content={"detail": "Options"}, status_code=200, headers=headers)

        # Control if the request needs authentication
        #The endpoints that start with /api are protected
        if "/api" not in request.url.path:
            #The endpoints that does not start with /api are unprotected and can be responded anyway.
            message = f"the endpoint {request.url.path} is unprotected. Access granted"

        else:
            #If the endpoint path include /api, it is protected and a valid token
            # must be provided in the request header
            if "cookie" not in request.headers:
                if request.url.path in temporaryUnprotectedEndpoints:
                    message = "the endpoint is temporarily unprotected and no token is provided"
                    message += "execution permit granted."
                else:
                    message = "the endpoint is protected but no token is provided"
                    # Return error 401
                    return JSONResponse({"detail":f"{message}"}, status_code=401)

            else:
                #Control if the token is valid
                print(f"Token is provided by the user: {request.headers['cookie']}")
                token = request.headers["cookie"].split("=")[1]
                print(f"token: {token}")
                message = f"the endpoint is protected and token is provided by user is: {token}"

                tokenValidation = verifyToken(token)
                isTokenValid = tokenValidation[0]
                tokenRenew = tokenValidation[1]
                # isTokenValid = verifyToken(token)
                if isTokenValid:
                    #the user is authenticated. Now it is time to check if the user is authorized to access the endpoint
                    #Extract the data from the token to use in the access control
                    tokenPayload = getTokenPayload(token)
                    requestType = request.method
                    endpoint = request.url.path

                    #Get the user role from the database
                    print(f"about to get user role for {tokenPayload['sub']}")
                    userRoleDict = await UserController.getUserRoleByUserName(tokenPayload['sub'])
                    print(f"userRoleDict is fetched successfully: {userRoleDict}")

                    # The user might have multiple roles. The roles are stored in a list.
                    userRole =  userRoleDict["roles"]       # a list of roles

                    #access includes the roles that can reach to a certain endpoint.
                    allowedRole = access[requestType][endpoint]


                    #Control if the user has the required role to access the endpoint
                    # If one of the roles is in the allowedRole list, the user can access the endpoint.
                    sufficientPrivilege: bool = False
                    for role in userRole:
                        if role in allowedRole:
                            sufficientPrivilege = True
                            break

                    if not sufficientPrivilege:
                        message = f"Access to {requestType}: {endpoint} rejected because {userRole[0]} is not in {allowedRole}"
                        return JSONResponse({"detail": f"{message}"}, status_code=401)
                    else:
                        message = (f"Access to {requestType}: {endpoint} authorized."
                                   f"UserRole is {userRole[0]} and allowed roles are {allowedRole}")
                else:
                    message = f"Access to a protected Endpoint rejected because {isTokenValid}"
                    return JSONResponse({"detail": f"{message}."}, status_code=401)

        print(message)
        print("Redirect to the next middleware or call the endpoint")
        response = await call_next(request)
        if tokenRenew:
            newToken = renewToken(token)
            response.set_cookie("jwt_token", newToken, httponly=True)
        return response