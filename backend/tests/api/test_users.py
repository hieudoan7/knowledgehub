from fastapi.testclient import TestClient


def register_user(
    client: TestClient,
    email: str = "john@example.com",
    password: str = "Password123!",
) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "John Doe",
        },
    )

    assert response.status_code == 201


def login_user(
    client: TestClient,
    email: str = "john@example.com",
    password: str = "Password123!",
) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_get_current_user(client: TestClient) -> None:
    """Authenticated user can retrieve their profile."""

    register_user(client)

    token = login_user(client)

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["email"] == "john@example.com"
    assert body["full_name"] == "John Doe"

    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_get_current_user_without_token(client: TestClient) -> None:
    response = client.get("/api/v1/users/me")

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Not authenticated"
    }


def test_get_current_user_invalid_token(client: TestClient) -> None:
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Could not validate credentials."
    }


