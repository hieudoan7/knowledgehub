import json
import os
from logging.config import fileConfig
from pathlib import Path

import boto3
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine, pool
from sqlalchemy.engine import URL

from app.db.base import Base
import app.models


# Load migration-specific environment variables.
BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env.migrator")

# Alembic configuration.
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url():
    """Retrieve migrator credentials from AWS Secrets Manager."""

    region = os.environ["AWS_REGION"]
    secret_name = os.environ["DB_MIGRATOR_SECRET"]

    client = boto3.client(
        "secretsmanager",
        region_name=region,
    )

    response = client.get_secret_value(
        SecretId=secret_name,
    )

    credentials = json.loads(response["SecretString"])

    return URL.create(
        drivername="postgresql+psycopg",
        username=credentials["username"],
        password=credentials["password"],
        host=os.environ["DB_HOST"],
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.environ["DB_NAME"],
        query={
            "sslmode": "verify-full",
            "sslrootcert": os.environ["RDS_CA_CERT"],
        },
    )


def run_migrations_offline() -> None:
    url = get_database_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        get_database_url(),
        poolclass=pool.NullPool,
    )

    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
            )

            with context.begin_transaction():
                context.run_migrations()
    finally:
        connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()