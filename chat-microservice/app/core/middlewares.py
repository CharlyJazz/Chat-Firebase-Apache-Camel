from app.core.logging import Logging
from fastapi import Request, Response
from typing import Callable
import json

async def request_middleware(request: Request, call_next: Callable):
    Logging.info(f"Request started at {request.url.path}")
    response = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    if response.status_code >= 400:
        Logging.error(f"{response.status_code} {json.loads(response_body.decode())['detail']} at {request.url.path}")
    else:
        Logging.info(f"{response.status_code} Request OK at {request.url.path}")
    Logging.info(f"Request ended at {request.url.path}")
    return Response(content=response_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type)