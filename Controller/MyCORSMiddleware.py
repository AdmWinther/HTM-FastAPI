import os

from starlette.middleware.base import BaseHTTPMiddleware


class MyCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print("via MyCORSMiddleware")
        response = await call_next(request)

        csrf_token = "your_generated_csrf_token"
        headers: dict = {"x-xsrf-token": csrf_token,
                         "Access-Control-Allow-Credentials": "true",
                         "Access-Control-Allow-Methods": "*",
                         "Access-Control-Allow-Headers": "*",
                         "Access-Control-Allow-Origin": f"{os.getenv('FRONTEND_URL')}"}

        response.headers.update(headers)
        return response