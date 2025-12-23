"""
체크인 기능 테스트
"""
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_checkin_flow():
    """체크인 → 테이블 조회 → 체크아웃 전체 플로우"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 1. 회원가입
        register_data = {
            "email": "checkin_test@example.com",
            "username": "checkinuser",
            "password": "test123",
            "tagline": "12층 테스터",
            "tags": "개발, 커피"
        }
        response = await client.post("/auth/register", json=register_data)
        assert response.status_code == 200
        
        # 2. 로그인
        login_data = {
            "username": "checkinuser",
            "password": "test123"
        }
        response = await client.post(
            "/auth/login",
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. 체크인 전: 테이블 조회 실패 (400)
        response = await client.get("/tables", headers=headers)
        assert response.status_code == 400
        assert "체크인이 필요합니다" in response.json()["detail"]
        
        # 4. 체크인
        checkin_data = {"location_code": "company-12f"}
        response = await client.post("/checkin", json=checkin_data, headers=headers)
        assert response.status_code == 201
        checkin = response.json()
        assert checkin["location_code"] == "company-12f"
        assert checkin["is_active"] == True
        
        # 5. 체크인 상태 확인
        response = await client.get("/checkin/status", headers=headers)
        assert response.status_code == 200
        status = response.json()
        assert status["is_checked_in"] == True
        assert status["location_code"] == "company-12f"
        
        # 6. 테이블 생성 (location_code 자동 적용)
        table_data = {
            "number": 101,
            "capacity": 4,
            "description": "12층 테스트 테이블"
        }
        response = await client.post("/tables", json=table_data, headers=headers)
        assert response.status_code == 201
        table = response.json()
        assert table["location_code"] == "company-12f"
        
        # 7. 테이블 조회 성공 (체크인 위치 기준)
        response = await client.get("/tables", headers=headers)
        assert response.status_code == 200
        tables = response.json()
        assert len(tables) > 0
        assert all(t["location_code"] == "company-12f" for t in tables)
        
        # 8. 체크아웃
        response = await client.delete("/checkin/checkout", headers=headers)
        assert response.status_code == 200
        
        # 9. 체크아웃 후: 체크인 상태 확인
        response = await client.get("/checkin/status", headers=headers)
        assert response.status_code == 200
        status = response.json()
        assert status["is_checked_in"] == False

@pytest.mark.asyncio
async def test_location_isolation():
    """다른 위치의 테이블은 보이지 않아야 함"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # 사용자 1: 12층 체크인
        register1 = {
            "email": "user12f@example.com",
            "username": "user12f",
            "password": "test123"
        }
        await client.post("/auth/register", json=register1)
        login1 = {"username": "user12f", "password": "test123"}
        response = await client.post("/auth/login", data=login1)
        token1 = response.json()["access_token"]
        headers1 = {"Authorization": f"Bearer {token1}"}
        
        await client.post("/checkin", json={"location_code": "company-12f"}, headers=headers1)
        
        # 사용자 2: 13층 체크인
        register2 = {
            "email": "user13f@example.com",
            "username": "user13f",
            "password": "test123"
        }
        await client.post("/auth/register", json=register2)
        login2 = {"username": "user13f", "password": "test123"}
        response = await client.post("/auth/login", data=login2)
        token2 = response.json()["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        await client.post("/checkin", json={"location_code": "company-13f"}, headers=headers2)
        
        # 12층 테이블 생성
        table12f = {"number": 201, "capacity": 4}
        response = await client.post("/tables", json=table12f, headers=headers1)
        assert response.status_code == 201
        
        # 13층 테이블 생성
        table13f = {"number": 202, "capacity": 4}
        response = await client.post("/tables", json=table13f, headers=headers2)
        assert response.status_code == 201
        
        # 12층 사용자: 12층 테이블만 보임
        response = await client.get("/tables", headers=headers1)
        tables_12f = response.json()
        assert all(t["location_code"] == "company-12f" for t in tables_12f)
        
        # 13층 사용자: 13층 테이블만 보임
        response = await client.get("/tables", headers=headers2)
        tables_13f = response.json()
        assert all(t["location_code"] == "company-13f" for t in tables_13f)
