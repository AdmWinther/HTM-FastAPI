import os
from tabnanny import verbose

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utility.JWTtoken import verifyToken, renewToken, getJwtTokenFromRequest, getUserRoleFromJwtTokenPayload
from utility.JWTtoken import isTokenAboutToExpire
from Controller.C00_EndpointAccess import accessRoles

def isCookiePresentInTheRequest(request: Request):
    if "cookie" not in request.headers:
        return False
    else:
        return True

def isProvidedCookieValid(request: Request):
    JwtToken = getJwtTokenFromRequest(request)
    isTokenValid = verifyToken(JwtToken)
    if isTokenValid:
        return True
    else:
        return False

async def IsUserRoleAllowedToAccessTheEndpoint(request: Request):
    JwtToken = getJwtTokenFromRequest(request)
    # Get the user role from the token payload
    # The user might have multiple roles. The roles are stored in a list.
    userRole = getUserRoleFromJwtTokenPayload(JwtToken)

    # Control Which useRoles are allowed to access the requested endpoint.
    requestType = request.method
    endpoint = request.url.path
    #Control if there is an ID at the end of the endpoint
    if "/id/" in endpoint:
        #Cut what ever that is after /id/
        endpoint = endpoint.split("/id/")[0]
        print(f"Endpoint is cut to {endpoint}")
    allowedRole = accessRoles[requestType][endpoint]

    # Control if the user has the required role to access the endpoint
    # If one of the roles is in the allowedRole list, the user can access the endpoint.
    sufficientPrivilege: bool = False
    for role in userRole:
        if role in allowedRole:
            sufficientPrivilege = True
            if verbose:
                print(f"Access to {requestType}: {endpoint} authorized."
                      f"UserRole is {userRole[0]} and allowed roles are {allowedRole}")
            break
    if verbose: print(f"Access to {requestType}: {endpoint} rejected because {userRole[0]} is not in {allowedRole}")
    return sufficientPrivilege


class MySecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        verbose: bool = os.getenv("VERBOSE") == "True"
        print(f"SecurityMiddleware is called for {request.method}: {request.url.path}")
        # todo: Delete the following line after the development is completed
        temporaryUnprotectedEndpoints = ["/api/user/reset"]

        # Control if the request needs authentication
        #The endpoints that start with /api are protected
        if "/api" not in request.url.path or request.url.path in temporaryUnprotectedEndpoints:
            #The endpoints that does not start with /api are unprotected and can be responded anyway.
            if verbose: print(f"the endpoint {request.url.path} is unprotected. Access granted")
            response = await call_next(request)
            return response
        else:
            # Check if any cookie is present in the request header for accessing a protected endpoint
            # Reject the Request if cookie is not present in the request header
            if isCookiePresentInTheRequest(request):
                if isProvidedCookieValid(request):
                    if await IsUserRoleAllowedToAccessTheEndpoint(request):
                        #print("Redirect to the next middleware or call the endpoint")
                        JwtToken = getJwtTokenFromRequest(request)
                        response = await call_next(request)
                        if isTokenAboutToExpire(JwtToken):
                            newJwtToken = renewToken(JwtToken)
                            response.set_cookie("jwt_token", newJwtToken, httponly=True)
                        return response
            return JSONResponse(content={"error": "Access Denied"}, status_code=401)

