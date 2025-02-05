from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(f"{request.method} {request.url.path} {process_time:.2f}s")
        return response

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logging.error(f"Error processing request: {str(e)}")
            raise 