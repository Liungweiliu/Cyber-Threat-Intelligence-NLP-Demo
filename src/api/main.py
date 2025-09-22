import time

from fastapi import FastAPI, Request

from src.api.endpoint import router

app = FastAPI(title="Cyber Threat Intelligence NLP Demo", version="0.0.1")

app.include_router(router, prefix="/api")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = " ".join(
        [str(round(process_time, 6)), "seconds"]
    )
    print(f"Request took: {process_time:.4f} seconds")
    return response
