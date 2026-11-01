from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.exceptions.handlers import register_exception_handlers
from app.core.logging import setup_logging

app = FastAPI(
    title="KnowledgeHub API",
    version="0.1.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
	    "https://knowledgehub-taupe.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
setup_logging()

app.include_router(api_router)

