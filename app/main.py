import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine, session_scope
from app.routers import auth, menu, table, order, match
from app.utils.seed import seed_menus

settings = get_settings()

def _is_testing() -> bool:
    return (
        os.getenv("PYTEST_CURRENT_TEST") is not None
        or os.getenv("TESTING") == "1"
        or os.getenv("ENVIRONMENT") == "test"
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    # [Startup] 서버 시작 시 실행
    if not _is_testing():
        Base.metadata.create_all(bind=engine)
        with session_scope() as session:
            seed_menus(session)
    yield
    # [Shutdown] 서버 종료 시 로직이 필요하면 여기에 작성

app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(table.router)
app.include_router(order.router)
app.include_router(match.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {"message": "Welcome to CoffeeKing backend"}
