from fastapi import FastAPI

from src.api.endpoint import router

app = FastAPI(title="Cyber Threat Intelligence NLP Demo", version="0.0.1")

app.include_router(router, prefix="/api")
