from fastapi import status


def test_tables_filtered_by_location(client, auth_headers):
    payload_12f = {"name": "12F-Table", "capacity": 2, "location_code": "company-12f"}
    payload_13f = {"name": "13F-Table", "capacity": 2, "location_code": "company-13f"}

    resp1 = client.post("/tables", json=payload_12f, headers=auth_headers)
    assert resp1.status_code == status.HTTP_201_CREATED, resp1.text

    resp2 = client.post("/tables", json=payload_13f, headers=auth_headers)
    assert resp2.status_code == status.HTTP_201_CREATED, resp2.text

    response = client.get("/tables", params={"location_code": "company-12f"}, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK, response.text
    tables = response.json()

    assert len(tables) == 1
    assert tables[0]["location_code"] == "company-12f"
    assert tables[0]["name"] == "12F-Table"
