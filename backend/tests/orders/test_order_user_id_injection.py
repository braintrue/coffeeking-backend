"""Ensure that order creation does not allow user_id tampering."""

from fastapi import status


def test_order_creation_ignores_user_id_from_payload(client, seed_base_data):
    menu = seed_base_data["menu"]
    table = seed_base_data["table"]
    user = seed_base_data["user"]

    # Authenticate to get a token
    login_response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "password123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_response.status_code == status.HTTP_200_OK
    token = login_response.json()["access_token"]

    response = client.post(
        "/orders/",
        json={
            "table_id": table.id,
            "items": [{"menu_id": menu.id, "quantity": 2}],
            "user_id": 999,
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == status.HTTP_201_CREATED
    order = response.json()
    assert order["user_id"] == user.id
    assert order["total_amount"] == menu.price * 2