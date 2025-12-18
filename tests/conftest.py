import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the application uses an isolated in-memory database for tests
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.database import Base, get_db  # noqa: E402
from app.main import app  # noqa: E402
from app.models.core import Menu, Table, User  # noqa: E402
from app.utils.security import get_password_hash  # noqa: E402

TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def seed_base_data(db_session):
    user = User(email="tester@example.com", hashed_password=get_password_hash("password123"), full_name="Test User")
    menu = Menu(name="Latte", description="Test latte", price=4.5)
    table = Table(name="A1", capacity=2)
    db_session.add_all([user, menu, table])
    db_session.commit()
    return {"user": user, "menu": menu, "table": table}
