from fastapi import FastAPI
from app.api.router import api_router
from app.exceptions.handlers import register_exception_handlers
from app.core.logging import setup_logging

app = FastAPI(
    title="KnowledgeHub API",
    version="0.1.0",
)

register_exception_handlers(app)
setup_logging()

app.include_router(api_router)

