import uuid
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from chatbot.core.logger import logger
from chatbot.database.session import (
    ScopedSessionLocal,
    reset_request_id,
    set_request_id,
)


class DBSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        request_id = str(uuid.uuid4())
        ctx_token = set_request_id(request_id)

        response = None

        try:
            try:
                # Create a new database session
                session = ScopedSessionLocal()
                request.state.db = session

                logger.info(
                    f"Successfully created the DB session for request id : {str(request_id)}"
                )
            except Exception as e:
                logger.error(
                    f"Error while creating the DB session for request id: {str(request_id)}, error : {str(e)}"
                )
                raise e

            response = await call_next(request)
            # Commit the transaction if no exceptions occurred
            request.state.db.commit()
        except Exception as e:
            logger.error(
                f"Exception occurred in DBSessionMiddleware request id : {str(request_id)} error: {str(e)}"
            )
            # Rollback the transaction if an exception occurred
            request.state.db.rollback()
            raise e
        finally:
            # Close the session
            if hasattr(request.state, "db"):
                request.state.db.close()
            reset_request_id(ctx_token)

        return response
