def test_upload(
    processed_document,
):
    assert processed_document["status"] == "ready"
