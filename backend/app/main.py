from fastapi import FastAPI
from app.api.router import api_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(
    title="KnowledgeHub API",
    version="0.1.0",
)

register_exception_handlers(app)

app.include_router(api_router)

