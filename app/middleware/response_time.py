import time
from fastapi import Request

async def add_response_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Response-Time"] = f"{elapsed_ms:.0f}ms"
    return response