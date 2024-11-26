import os

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class MyCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"MyCORSMiddleware is called for {request.method}: {request.url.path}")

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


        response = await call_next(request)

        headers = self.return_headers()
        response.headers.update(headers)
        return response

    @staticmethod
    def return_headers():
        csrf_token = "your_generated_csrf_token"
        # headers: dict = {"x-xsrf-token": csrf_token,
        headers: dict = {"Access-Control-Allow-Credentials": "true",
                         "Access-Control-Allow-Methods": "DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT",
                         "Access-Control-Allow-Headers": "Content-Type, X-XSRF-TOKEN, X-CSRF-TOKEN, credentials",
                         "Content-Type": "text/plain; charset=utf-8",
                         "Access-Control-Allow-Origin": f"{os.getenv('FRONTEND_URL')}"}
        return headers