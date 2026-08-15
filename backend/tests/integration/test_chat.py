def test_chat_answers_question_from_document(
    client,
    auth_headers,
    processed_document,
):
    response = client.post(
        f"/api/v1/documents/{processed_document['id']}/chat",
        json={
            "question": "What programming languages does the candidate know?",
        },
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert isinstance(data["answer"], str)
    assert len(data["answer"]) > 0

    answer = data["answer"].lower()

    assert any(
        language in answer
        for language in [
            "python",
            "golang",
            "django",
            "kafka",
        ]
    )

def test_chat_history_is_persisted(
    client,
    auth_headers,
    processed_document,
):
    document_id = processed_document["id"]

    chat_response = client.post(
        f"/api/v1/documents/{document_id}/chat",
        json={
            "question": "What programming languages does the candidate know?",
        },
        headers=auth_headers,
    )

    assert chat_response.status_code == 200

    chat_data = chat_response.json()

    history_response = client.get(
        f"/api/v1/documents/{document_id}/chat/history",
        headers=auth_headers,
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) >= 1

    message = history[-1]

    assert message["question"] == (
        "What programming languages does the candidate know?"
    )

    assert message["answer"] == chat_data["answer"]
    assert message["sources"] == chat_data["sources"]