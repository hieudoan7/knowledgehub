from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/knowledgehub_test"

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    Base.metadata.drop_all(bind=engine)


def get_test_db() -> Session:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

