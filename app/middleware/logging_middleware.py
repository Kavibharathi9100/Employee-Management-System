from typing import Callable, Awaitable
import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:

        start_time = time.perf_counter()

        logger.info(
            "Incoming Request | Method=%s | Path=%s | Client=%s",
            request.method,
            request.url.path,
            request.client.host if request.client else "Unknown"
        )

        try:
            response = await call_next(request)

        except Exception as e:
            logger.exception(
                "Unhandled Exception: %s",
                str(e)
            )
            raise

        process_time = (time.perf_counter() - start_time) * 1000

        logger.info(
            "Outgoing Response | Status=%s | Time=%.2f ms",
            response.status_code,
            process_time
        )

        return response