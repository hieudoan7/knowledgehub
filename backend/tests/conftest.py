import pytest
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.services.background_tasks import BackgroundTaskService
from .database import TestingSessionLocal
from app.db.session import SessionLocal

from .database import (
    engine,
    get_test_db,
)

# Register fixtures
from .fixtures.auth import *      # noqa: F401,F403
from .fixtures.document import *  # noqa: F401,F403


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = get_test_db

    BackgroundTaskService.session_factory = TestingSessionLocal

    with TestClient(app) as client:
        yield client

    BackgroundTaskService.session_factory = SessionLocal

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)
