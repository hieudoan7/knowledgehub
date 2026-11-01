import json
from logging.config import fileConfig

import boto3
from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import pool

from app.core.config import settings
from app.db.base import Base
import app.models


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_database_url():
    """Retrieve migrator credentials from AWS Secrets Manager."""
    client = boto3.client(
        "secretsmanager",
        region_name=settings.AWS_REGION,
    )

    response = client.get_secret_value(
        SecretId=settings.DB_MIGRATOR_SECRET,
    )

    credentials = json.loads(response["SecretString"])

    return URL.create(
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

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()