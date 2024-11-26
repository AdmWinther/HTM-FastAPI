import os

from fastapi import Request
from pyexpat.errors import messages
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from Controller import UserController
from Controller.JWTtoken import verifyToken, getTokenPayload, renewToken, getJwtTokenFromRequestHeader, \
    getCsrfTokenFromRequestHeader
from Controller.MyCORSMiddleware import MyCORSMiddleware
from Controller.EndpointAccess import accessRoles


async def controlToken(JwtToken: str):
    print(f"JwtToken: {JwtToken}")
    # Verify the token, the result of validation is a tuple,
    # the first element is a boolean value that shows if the token is valid or not,
    # the second element is a boolean value that shows if the token is about to be expired.
    tokenValidation = verifyToken(JwtToken)
    isTokenValid = tokenValidation[0]
    tokenRenew = tokenValidation[1]
    return isTokenValid, tokenRenew

def rejectIfRequestCookieIsNotPresent(request: Request):
    if "cookie" not in request.headers:
        return JSONResponse({"detail": "No cookie in the request header."}, status_code=401)
    else:
        return None


class MySecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"SecurityMiddleware is called for {request.method}: {request.url.path}")
        # todo: Delete the following line after the development is completed
        temporaryUnprotectedEndpoints = ["/api/user/reset"]

        token = ""

        # the variable tokenRenew is used to control the token renewal.
        # If the token is about to be expired the tokenRenew is set to True when token is verified.
        # token will be renewed only if the token lifetime is less than the renewal time.
        tokenRenew: bool = False




        # Control if the request needs authentication
        #The endpoints that start with /api are protected
        if "/api" not in request.url.path or request.url.path in temporaryUnprotectedEndpoints:
            # ************************************************************************************************
            # ***********************  response to Public (no authentication) Request  ***********************
            # ************************************************************************************************
            #The endpoints that does not start with /api are unprotected and can be responded anyway.
            message = f"the endpoint {request.url.path} is unprotected. Access granted"

        else:
            # Check if any cookie is present in the request header for accessing a protected endpoint
            # Reject the Request if cookie is not present in the request header
            rejectIfRequestCookieIsNotPresent(request)

            # ************************************************************************************************
            # ************************  Validate the cookie for protected endpoints  *************************
            # ************************************************************************************************
            JwtToken = getJwtTokenFromRequestHeader(request)
            isTokenValid, tokenRenew = await controlToken(JwtToken)
            if isTokenValid:
                sufficientPrivilege, message = await self.controlUserAccessLevel(JwtToken, request)

                if not sufficientPrivilege:
                    return JSONResponse({"detail": f"{message}"}, status_code=401)

            else:
                message = f"Access to a protected Endpoint rejected because isTokenValid: {isTokenValid}"
                return JSONResponse({"detail": f"{message}."}, status_code=401)

        print("Redirect to the next middleware or call the endpoint")
        response = await call_next(request)
        if tokenRenew:
            newJwtToken = renewToken(JwtToken)
            response.set_cookie("jwt_token", newJwtToken, httponly=True)
        return response

    async def controlUserAccessLevel(self, JwtToken, request):
        # the user is authenticated. Now it is time to check if the user is authorized to access the endpoint
        # Extract the data from the token to use in the access control
        tokenPayload = getTokenPayload(JwtToken)
        requestType = request.method
        endpoint = request.url.path
        # Get the user role from the token payload
        print(f"about to get user role for {tokenPayload['sub']} from token payload")
        userRoleDict = tokenPayload["role"]
        print(f"userRoleDict is fetched successfully: {userRoleDict}")
        # The user might have multiple roles. The roles are stored in a list.
        # userRole =  userRoleDict["roles"]       # a list of roles
        userRole = userRoleDict  # if userRole is read from token payload, it is already an array not a dict
        # access includes the roles that can reach to a certain endpoint.
        allowedRole = accessRoles[requestType][endpoint]
        # Control if the user has the required role to access the endpoint
        # If one of the roles is in the allowedRole list, the user can access the endpoint.
        sufficientPrivilege: bool = False
        for role in userRole:
            if role in allowedRole:
                sufficientPrivilege = True
                message = (f"Access to {requestType}: {endpoint} authorized."
                           f"UserRole is {userRole[0]} and allowed roles are {allowedRole}")
                break
        message = f"Access to {requestType}: {endpoint} rejected because {userRole[0]} is not in {allowedRole}"
        return sufficientPrivilege, message