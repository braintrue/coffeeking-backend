# tests/conftest.py
import os
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# ---------------------------------------------------------
# 0) 반드시 app.* import 전에 테스트 DB로 고정
#    in-memory를 "프로세스/세션 간 공유"하려면 sqlite:// + StaticPool이 안전함
# ---------------------------------------------------------
os.environ["TESTING"] = "1"
TEST_DB_URL = "sqlite://"
os.environ["DATABASE_URL"] = TEST_DB_URL

# ---------------------------------------------------------
# 1) 앱/DB 모듈 로드 (모델 등록 포함)
# ---------------------------------------------------------
import app.models  # noqa: F401  (모델 등록)
import app.database as db_module  # noqa: E402
from app.database import Base, get_db  # noqa: E402
from app.main import app as fastapi_app  # noqa: E402

from app.models.core import Menu, Table, User  # noqa: E402
from app.utils.security import get_password_hash  # noqa: E402

# ---------------------------------------------------------
# 2) 테스트용 엔진/세션 (StaticPool로 in-memory 유지)
# ---------------------------------------------------------
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False,)

# app.database가 들고 있는 전역 engine/SessionLocal을 테스트용으로 교체
db_module.engine = engine
db_module.SessionLocal = TestingSessionLocal


# ---------------------------------------------------------
# 3) DB 초기화 (테이블 생성)
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def setup_database():
    Base.metadata.create_all(bind=engine)
    try:
        yield
    finally:
        Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------
# 4) get_db override (FastAPI dependency)
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def client(setup_database):
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    fastapi_app.dependency_overrides[get_db] = override_get_db

    with TestClient(fastapi_app) as c:
        yield c

    fastapi_app.dependency_overrides.clear()


# ---------------------------------------------------------
# 5) 테스트 유저 생성 + Authorization 헤더 제공
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def test_user(setup_database):
    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == "testuser@example.com").first()
        if user is None:
            user = User(
                email="testuser@example.com",
                hashed_password=get_password_hash("Password123!"),
                full_name="Test User",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()


@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    # 로그인해서 토큰 받기
    resp = client.post(
        "/auth/login",
        data={"username": test_user.email, "password": "Password123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------
# 6) 주문 테스트가 기대하는 기본 데이터(menu/user/table)
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def seed_base_data(setup_database):
    db = TestingSessionLocal()
    try:
        # Menu
        menu = db.query(Menu).first()
        if menu is None:
            menu = Menu(
                name="Americano",
                description="Coffee",
                price=3.5,
                is_available=True,
            )
            db.add(menu)
            db.commit()
            db.refresh(menu)

        # User
        user = db.query(User).filter(User.email == "seeduser@example.com").first()
        if user is None:
            user = User(
                email="seeduser@example.com",
                hashed_password=get_password_hash("Password123!"),
                full_name="Seed User",
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Table (모델 컬럼에 맞춰 "있는 필드만" 안전하게 채움)
        table = db.query(Table).first()
        if table is None:
            cols = {c.name for c in Table.__table__.columns}

            payload = {}
            if "name" in cols:
                payload["name"] = "12F-1"
            if "number" in cols:
                payload["number"] = 1
            if "table_number" in cols:
                payload["table_number"] = 1

            # location_code는 없다고 했으니, 존재하는 location 관련 컬럼만 넣기
            if "location" in cols:
                payload["location"] = "company-12f"
            if "floor" in cols:
                payload["floor"] = "12f"
            if "is_active" in cols:
                payload["is_active"] = True
            if "is_available" in cols:
                payload["is_available"] = True

            table = Table(**payload)
            db.add(table)
            db.commit()
            db.refresh(table)

        return {"menu_id": menu.id, "user_id": user.id, "table_id": table.id}
    finally:
        db.close()


