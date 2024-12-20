import os
import json

from starlette.responses import JSONResponse

from Controller.C00_EndpointAccess import csrfProtection

from starlette.middleware.base import BaseHTTPMiddleware

from Service.CSRFService import CSRFService


class MyCSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        verbose: bool = os.getenv("VERBOSE") == "True"
        print(f"MyCsrfMiddleware is called for {request.method}: {request.url.path}")

        #************************************************************************************************
        #*********************************  request destination control  ********************************
        #************************************************************************************************
        # Control if the requested endpoint is CSRF protected
        requestType = request.method
        endpoint = request.url.path
        # Control if there is an ID at the end of the endpoint
        if "/id/" in endpoint:
            # Cut what ever that is after /id/
            endpoint = endpoint.split("/id/")[0]
            print(f"Endpoint is cut to {endpoint}")

        IsEndpointCsrfProtected: bool = csrfProtection[requestType][endpoint]
        if IsEndpointCsrfProtected:
            #The endpoint is CSRF protected, therefore the request must contain the CSRF token in the body
            requestBody = await request.body()
            body_data = json.loads(requestBody)
            if "X-XSRF-TOKEN" not in body_data:
                return JSONResponse({"error": "CSRF Token is missing in the request body"}, status_code=401)
            else:
                CsrfToken = body_data["X-XSRF-TOKEN"]
                #print(f"CSRF Token is: {CsrfToken}")
                #Control if the CSRF token is valid
                isCsrfTokenValid = await CSRFService.validateCSRFToken(request, CsrfToken)
                if isCsrfTokenValid:
                    #print("The endpoint is CSRF protected and a valid token is provided, redirect to the next")
                    response = await call_next(request)
                    return response
                else:
                    return JSONResponse({"error": "CSRF Token is invalid"}, status_code=401)
        else:
            #print("The endpoint is not CSRF protected, redirect to the next")
            response = await call_next(request)
            return response
