import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.db.base import Base
from app.main import app

from tests.database import (
    engine,
    get_test_db,
)


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = get_test_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)
