from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# Create a single SQLAlchemy engine for the application.
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

# Factory for creating new database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    A new session is created for each request and is automatically
    closed when the request finishes.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
