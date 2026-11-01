
import json
import os
import secrets
import sys

import boto3
import psycopg
from botocore.exceptions import ClientError
from psycopg import sql


REGION = os.getenv("AWS_REGION", "ap-southeast-2")

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "knowledgehub")
ADMIN_SECRET = os.getenv(
    "DB_ADMIN_SECRET",
    "knowledgehub/production/admin",
)
CA_CERT = os.getenv(
    "RDS_CA_CERT",
    "/opt/knowledgehub/certs/global-bundle.pem",
)

APP_SECRET = "knowledgehub/production/app"
MIGRATOR_SECRET = "knowledgehub/production/migrator"

APP_USER = "kh_app"
MIGRATOR_USER = "kh_migrator"

secrets_client = boto3.client("secretsmanager", region_name=REGION)


def get_secret(secret_name):
    response = secrets_client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])


def get_or_create_credentials(secret_name, username):
    """Reuse existing credentials, or create them once and store them."""
    try:
        response = secrets_client.describe_secret(SecretId=secret_name)

        if response.get("DeletedDate"):
            raise RuntimeError(
                f"Secret {secret_name} is scheduled for deletion."
            )

        return get_secret(secret_name)

    except secrets_client.exceptions.ResourceNotFoundException:
        credentials = {
            "username": username,
            "password": secrets.token_urlsafe(32),
        }

        try:
            secrets_client.create_secret(
                Name=secret_name,
                Description=f"KnowledgeHub production credentials for {username}",
                SecretString=json.dumps(credentials),
            )
            print(f"Created secret: {secret_name}")
            return credentials

        except ClientError as error:
            if error.response["Error"]["Code"] == "ResourceExistsException":
                # Another provisioning run created it concurrently.
                return get_secret(secret_name)
            raise


def connect(database, username, password):
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=database,
        user=username,
        password=password,
        sslmode="verify-full",
        sslrootcert=CA_CERT,
    )


def ensure_role(cursor, username, password):
    cursor.execute(
        "SELECT 1 FROM pg_roles WHERE rolname = %s",
        (username,),
    )

    if cursor.fetchone():
        cursor.execute(
            sql.SQL("ALTER ROLE {} WITH LOGIN PASSWORD {}").format(
                sql.Identifier(username),
                sql.Literal(password),
            )
        )
        print(f"Updated role: {username}")
    else:
        cursor.execute(
            sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD {}").format(
                sql.Identifier(username),
                sql.Literal(password),
            )
        )
        print(f"Created role: {username}")


def ensure_database(admin_username):
    with connect("postgres", admin_username, admin_password) as conn:
        conn.autocommit = True

        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (DB_NAME,),
            )

            if cursor.fetchone():
                print(f"Database already exists: {DB_NAME}")
            else:
                cursor.execute(
                    sql.SQL("CREATE DATABASE {}").format(
                        sql.Identifier(DB_NAME)
                    )
                )
                print(f"Created database: {DB_NAME}")


def configure_database(admin_username, app_password, migrator_password):
    with connect(DB_NAME, admin_username, admin_password) as conn:
        with conn.cursor() as cursor:
            # Install pgvector in this database.
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # Let the migration user create and own application tables.
            cursor.execute(
                sql.SQL("GRANT CONNECT ON DATABASE {} TO {}, {}").format(
                    sql.Identifier(DB_NAME),
                    sql.Identifier(APP_USER),
                    sql.Identifier(MIGRATOR_USER),
                )
            )

            cursor.execute(
                sql.SQL(
                    "GRANT USAGE, CREATE ON SCHEMA public TO {}"
                ).format(sql.Identifier(MIGRATOR_USER))
            )

            cursor.execute(
                sql.SQL(
                    "GRANT USAGE ON SCHEMA public TO {}"
                ).format(sql.Identifier(APP_USER))
            )

            # Existing tables and sequences.
            cursor.execute(
                sql.SQL(
                    "GRANT SELECT, INSERT, UPDATE, DELETE "
                    "ON ALL TABLES IN SCHEMA public TO {}"
                ).format(sql.Identifier(APP_USER))
            )

            cursor.execute(
                sql.SQL(
                    "GRANT USAGE, SELECT ON ALL SEQUENCES "
                    "IN SCHEMA public TO {}"
                ).format(sql.Identifier(APP_USER))
            )

            # Automatically grant app permissions on future migration objects.
            cursor.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA public "
                    "GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO {}"
                ).format(
                    sql.Identifier(MIGRATOR_USER),
                    sql.Identifier(APP_USER),
                )
            )

            cursor.execute(
                sql.SQL(
                    "ALTER DEFAULT PRIVILEGES FOR ROLE {} IN SCHEMA public "
                    "GRANT USAGE, SELECT ON SEQUENCES TO {}"
                ).format(
                    sql.Identifier(MIGRATOR_USER),
                    sql.Identifier(APP_USER),
                )
            )

        conn.commit()

    print("Configured database permissions and pgvector.")


def main():
    global admin_password

    if not os.path.isfile(CA_CERT):
        raise FileNotFoundError(f"RDS CA certificate not found: {CA_CERT}")

    print("Retrieving RDS admin credentials...")
    admin_credentials = get_secret(ADMIN_SECRET)
    admin_username = admin_credentials["username"]
    admin_password = admin_credentials["password"]

    print("Preparing application credentials...")
    app_credentials = get_or_create_credentials(APP_SECRET, APP_USER)
    migrator_credentials = get_or_create_credentials(
        MIGRATOR_SECRET,
        MIGRATOR_USER,
    )

    if app_credentials["username"] != APP_USER:
        raise RuntimeError("Unexpected username in app secret.")

    if migrator_credentials["username"] != MIGRATOR_USER:
        raise RuntimeError("Unexpected username in migrator secret.")

    print("Connecting to RDS and ensuring roles exist...")
    with connect("postgres", admin_username, admin_password) as conn:
        with conn.cursor() as cursor:
            ensure_role(
                cursor,
                APP_USER,
                app_credentials["password"],
            )
            ensure_role(
                cursor,
                MIGRATOR_USER,
                migrator_credentials["password"],
            )
        conn.commit()

    print("Ensuring application database exists...")
    ensure_database(admin_username)

    print("Configuring application database...")
    configure_database(
        admin_username,
        app_credentials["password"],
        migrator_credentials["password"],
    )

    print("\nDatabase provisioning completed successfully.")
    print(f"Database: {DB_NAME}")
    print(f"Application user: {APP_USER}")
    print(f"Migration user: {MIGRATOR_USER}")
    print("Credentials are stored in AWS Secrets Manager.")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"\nProvisioning failed: {error}", file=sys.stderr)
        sys.exit(1)
