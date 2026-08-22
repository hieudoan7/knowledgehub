import boto3

from app.storage.base import StorageService


class S3StorageService(StorageService):
    """Store files in an Amazon S3 bucket."""

    def __init__(
        self,
        *,
        bucket_name: str,
        region_name: str,
        prefix: str = "",
    ) -> None:
        self.bucket_name = bucket_name
        self.prefix = prefix.strip("/")

        self.client = boto3.client(
            "s3",
            region_name=region_name,
        )

    def _key(self, storage_path: str) -> str:
        """Build the S3 object key."""
        if self.prefix:
            return f"{self.prefix}/{storage_path}"

        return storage_path

    def save(
        self,
        *,
        filename: str,
        content: bytes,
    ) -> str:
        """Save a file to S3 and return its storage key."""

        key = self._key(filename)

        self.client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=content,
        )

        return filename

    def delete(
        self,
        storage_path: str,
    ) -> None:
        """Delete a file from S3."""

        self.client.delete_object(
            Bucket=self.bucket_name,
            Key=self._key(storage_path),
        )

    def exists(
        self,
        storage_path: str,
    ) -> bool:
        """Check whether a file exists in S3."""

        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=self._key(storage_path),
            )
            return True
        except self.client.exceptions.ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code in {"404", "NoSuchKey", "NotFound"}:
                return False

            raise

    def read(
        self,
        storage_path: str,
    ) -> bytes:
        """Read a file from S3."""

        response = self.client.get_object(
            Bucket=self.bucket_name,
            Key=self._key(storage_path),
        )

        return response["Body"].read()