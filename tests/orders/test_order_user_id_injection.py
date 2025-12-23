from fastapi import status


def test_order_creation_ignores_user_id_from_payload(client, seed_base_data):
    menu_id = seed_base_data["menu_id"]
    table_id = seed_base_data["table_id"]
    user_id = seed_base_data["user_id"]

    response = client.post(
        "/orders/",
        json={
            "table_id": table_id,
            "items": [{"menu_id": menu_id, "quantity": 2}],
            "user_id": 999,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    order = response.json()
    assert order["user_id"] == user_id
