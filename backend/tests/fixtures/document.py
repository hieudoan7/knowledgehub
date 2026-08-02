import pytest

from tests.helpers.files import get_test_file
from tests.helpers.wait_for_document import wait_for_document_ready


@pytest.fixture
def processed_document(
    client,
    auth_headers,
):
    pdf_path = get_test_file("resume.pdf")

    with pdf_path.open("rb") as file:
        response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": (
                    "resume.pdf",
                    file,
                    "application/pdf",
                ),
            },
            headers=auth_headers,
        )

    assert response.status_code == 201

    document = response.json()

    wait_for_document_ready(
        client=client,
        auth_headers=auth_headers,
        document_id=document["id"],
    )

    # Fetch the latest state
    response = client.get(
        f"/api/v1/documents/{document['id']}",
        headers=auth_headers,
    )
    print(response.status_code)
    print(response.json())

    assert response.status_code == 200

    return response.json()