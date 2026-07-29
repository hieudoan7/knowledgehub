from fastapi.testclient import TestClient


def register_user(
    client: TestClient,
    email: str = "john@example.com",
    password: str = "Password123!",
) -> None:
    """Helper function to create a user for authentication tests."""

    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "John Doe",
        },
    )

    assert response.status_code == 201

def test_login_success(client: TestClient) -> None:
    register_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"

def test_login_invalid_password(client: TestClient) -> None:
    register_user(client)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "john@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid email or password.",
    }

def test_login_unknown_email(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid email or password.",
    }
