import json
from collections.abc import Generator

import boto3
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


def get_database_credentials() -> dict:
    """Retrieve database credentials from AWS Secrets Manager."""
    client = boto3.client(
        "secretsmanager",
        region_name=settings.AWS_REGION,
    )

    response = client.get_secret_value(
        SecretId=settings.DB_APP_SECRET,
    )

    return json.loads(response["SecretString"])


# Fetch credentials once when the application starts.
credentials = get_database_credentials()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=credentials["username"],
    password=credentials["password"],
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    query={
        "sslmode": "verify-full",
        "sslrootcert": settings.RDS_CA_CERT,
    },
)

# Create a single SQLAlchemy engine.
engine = create_engine(
    database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()