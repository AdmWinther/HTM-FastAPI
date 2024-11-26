from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class MyOptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"MyOptionMiddleware is called for {request.method}: {request.url.path}")

        # ************************************************************************************************
        # *********************************  response to Option Request  *********************************
        # ************************************************************************************************
        # Control the request origin, the request must come from the frontend domain.
        if request.method == "OPTIONS":
            # Respond to preflight requests with the appropriate CORS headers and status code 200
            # print(f"I am sending a 200 response to request {request.method}: {request.url.path}")
            return JSONResponse(content={"detail": "Options"}, status_code=200)
        else:
            response = await call_next(request)
            return response

