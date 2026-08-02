import time
from uuid import UUID

from fastapi.testclient import TestClient


def wait_for_document_ready(
    client: TestClient,
    auth_headers: dict[str, str],
    document_id: UUID,
    timeout: int = 30,
) -> None:
    deadline = time.time() + timeout

    while time.time() < deadline:
        response = client.get(
            f"/api/v1/documents/{document_id}/status",
            headers=auth_headers,
        )

        assert response.status_code == 200

        status = response.json()["status"]

        if status == "ready":
            return

        if status == "failed":
            raise AssertionError("Document processing failed.")

        time.sleep(0.2)

    raise TimeoutError("Document was never processed.")
