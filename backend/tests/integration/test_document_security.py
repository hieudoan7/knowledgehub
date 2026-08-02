def test_search_other_users_document_returns_404(
    client,
    processed_document,
    another_auth_headers,
):
    response = client.post(
        f"/api/v1/documents/{processed_document['id']}/search",
        json={
            "query": "Python",
            "limit": 5,
        },
        headers=another_auth_headers,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document not found.",
    }


def test_chat_other_users_document_returns_404(
    client,
    processed_document,
    another_auth_headers,
):
    response = client.post(
        f"/api/v1/documents/{processed_document['id']}/chat",
        json={
            "question": "What programming languages does the candidate know?",
        },
        headers=another_auth_headers,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document not found.",
    }


def test_get_document_other_users_document_returns_404(
    client,
    processed_document,
    another_auth_headers,
):
    response = client.get(
        f"/api/v1/documents/{processed_document['id']}",
        headers=another_auth_headers,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document not found.",
    }


def test_get_document_status_other_users_document_returns_404(
    client,
    processed_document,
    another_auth_headers,
):
    response = client.get(
        f"/api/v1/documents/{processed_document['id']}/status",
        headers=another_auth_headers,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Document not found.",
    }
