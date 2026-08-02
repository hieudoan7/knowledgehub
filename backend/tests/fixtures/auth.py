import pytest


@pytest.fixture
def registered_user(client):
    payload = {
        "email": "test@example.com",
        "password": "Password123!",
        "full_name": "Test User",
    }

    client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    return payload


@pytest.fixture
def access_token(
    client,
    registered_user,
):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    return response.json()["access_token"]


@pytest.fixture
def auth_headers(
    access_token,
):
    return {
        "Authorization": f"Bearer {access_token}",
    }

@pytest.fixture
def another_registered_user(client):
    payload = {
        "email": "another@example.com",
        "password": "Password123!",
        "full_name": "Another User",
    }

    client.post(
        "/api/v1/auth/register",
        json=payload,
    )

    return payload


@pytest.fixture
def another_access_token(
    client,
    another_registered_user,
):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": another_registered_user["email"],
            "password": another_registered_user["password"],
        },
    )

    return response.json()["access_token"]


@pytest.fixture
def another_auth_headers(
    another_access_token,
):
    return {
        "Authorization": f"Bearer {another_access_token}",
    }