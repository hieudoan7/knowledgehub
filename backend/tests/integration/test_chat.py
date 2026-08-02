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
