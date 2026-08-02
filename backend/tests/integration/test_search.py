def test_search_returns_relevant_chunks(
    client,
    auth_headers,
    processed_document,
):
    response = client.post(
        f"/api/v1/documents/{processed_document['id']}/search",
        json={
            "query": "What programming languages does the candidate know?",
            "limit": 5,
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    results = response.json()

    assert len(results) > 0

    contents = " ".join(
        chunk["content"]
        for chunk in results
    )

    assert "Python" in contents