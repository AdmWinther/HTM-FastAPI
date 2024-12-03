import os
import json

from starlette.responses import JSONResponse

from Controller.EndpointAccess import csrfProtection

from starlette.middleware.base import BaseHTTPMiddleware

from Service.CSRFService import CSRFService


class MyCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        verbose: bool = os.getenv("VERBOSE") == "True"
        print(f"My CSRF Middleware is called for {request.method}: {request.url.path}")

        #************************************************************************************************
        #*********************************  request destination control  ********************************
        #************************************************************************************************
        # Control if the requested endpoint is CSRF protected
        requestType = request.method
        endpoint = request.url.path

        IsEndpointCsrfProtected: bool = csrfProtection[requestType][endpoint]
        if IsEndpointCsrfProtected:
            #The endpoint is CSRF protected, therefore the request must contain the CSRF token in the body
            requestBody = await request.body()
            body_data = json.loads(requestBody)
            if "X-XSRF-TOKEN" not in body_data:
                return JSONResponse({"detail": "CSRF Token is missing in the request body"}, status_code=401)
            else:
                CsrfToken = body_data["X-XSRF-TOKEN"]
                print(f"CSRF Token is: {CsrfToken}")
                #Control if the CSRF token is valid
                if CSRFService.validateCSRFToken(request, CsrfToken):
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse({"detail": "CSRF Token is invalid"}, status_code=401)
        else:
            response = await call_next(request)
            return response
