"""Tests for the authentication flow (registration and login)."""

from fastapi import status


def test_register_and_login_flow(client):
    register_payload = {
        "email": "newuser@example.com",
        "password": "securepass",
        "full_name": "New User",
    }

    register_response = client.post("/auth/register", json=register_payload)
    assert register_response.status_code == status.HTTP_201_CREATED
    registered_user = register_response.json()
    assert registered_user["email"] == register_payload["email"]

    login_response = client.post(
        "/auth/login",
        data={"username": register_payload["email"], "password": register_payload["password"]},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == status.HTTP_200_OK
    login_payload = login_response.json()
    assert "access_token" in login_payload
    assert login_payload["token_type"] == "bearer"