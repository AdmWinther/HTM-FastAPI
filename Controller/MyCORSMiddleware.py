import os

from starlette.middleware.base import BaseHTTPMiddleware


class MyCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # print("via MyCORSMiddleware")
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
                         "Access-Control-Allow-Headers": "Content-Type, X-XSRF-TOKEN, X-CSRF-TOKEN, Authorization",
                         "Content-Type": "text/plain; charset=utf-8",
                         "Access-Control-Allow-Origin": f"{os.getenv('FRONTEND_URL')}"}
        return headers