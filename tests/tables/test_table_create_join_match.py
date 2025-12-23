from fastapi import status


def test_create_join_sets_matched(client, auth_headers):
    create_resp = client.post(
        "/tables",
        json={"name": "12F-Match", "capacity": 2, "location_code": "company-12f"},
        headers=auth_headers,
    )
    assert create_resp.status_code == status.HTTP_201_CREATED, create_resp.text
    table = create_resp.json()

    join_resp = client.post(f"/tables/{table['id']}/join", headers=auth_headers)
    assert join_resp.status_code == status.HTTP_200_OK, join_resp.text
    result = join_resp.json()

    assert result["table"]["status"] == "matched"
    assert result["table"]["current_count"] == 2
    assert f"{table['id']}번 테이블로 가세요" in result["message"]
