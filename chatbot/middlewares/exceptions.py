import traceback
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
from fastapi.responses import JSONResponse
from starlette.requests import Request
from fastapi import HTTPException, status


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except HTTPException as e:
            print(e)
            traceback.print_exc()

            response = JSONResponse(
                status_code=e.status_code,
                content={"detail": {"error": e.detail}},
            )
        except Exception as e:
            print(e)
            traceback.print_exc()

            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": {"error": str(e)}},
            )

        return response
