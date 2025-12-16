from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, menu, table, order, match
from app.utils.seed import seed_menus

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

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


@app.on_event("startup")
def on_startup():
    from app.database import session_scope

    with session_scope() as session:
        seed_menus(session)


@app.get("/")
def read_root():
    return {"message": "Welcome to CoffeeKing backend"}
