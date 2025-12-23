import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine, SessionLocal, session_scope
from app.routers import auth, menu, table, order, match
from app.utils.seed import seed_menus

settings = get_settings()

# ✅ DB 테이블 생성 (운영/로컬 실행 시)
# 테스트에서는 conftest에서 별도 엔진/세션을 쓰므로, 여기 create_all은 큰 문제 없지만
# in-memory DB면 엔진이 다르면 테이블이 안 생길 수 있음.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)


@app.get("/health", include_in_schema=True)
def health_check():
    return {"status": "ok"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(table.router)
app.include_router(order.router)
app.include_router(match.router)


def _is_testing() -> bool:
    """
    pytest 실행 중이면 startup seed를 막아 CI에서 'no such table' 같은 오류를 피한다.
    - tests/conftest.py에서 필요한 seed는 fixture에서 직접 넣는다.
    """
    return (
        os.getenv("PYTEST_CURRENT_TEST") is not None
        or os.getenv("TESTING") == "1"
        or os.getenv("ENVIRONMENT") == "test"
    )


@app.on_event("startup")
def on_startup():
    if _is_testing():
        return

    Base.metadata.create_all(bind=engine)
    with session_scope() as session:
        seed_menus(session)

@app.get("/")
def read_root():
    return {"message": "Welcome to CoffeeKing backend"}
