"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.routers import auth, menu, table, order, match
from app.utils.seed import seed_menus

# Initialise settings and create all database tables up front.  Normally you
# might handle migrations separately but for an MVP ``create_all`` is
# acceptable.
settings = get_settings()
Base.metadata.create_all(bind=engine)

# Create the FastAPI application.  The title is taken from the settings.
app = FastAPI(title=settings.app_name)

# Configure CORS.  In a production deployment you would restrict origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routers with the application.  Each router defines its own
# prefix and tag grouping.
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(table.router)
app.include_router(order.router)
app.include_router(match.router)


@app.on_event("startup")
def on_startup() -> None:
    """Seed menus when the application starts."""
    from app.database import session_scope

    with session_scope() as session:
        seed_menus(session)


@app.get("/")
def read_root() -> dict[str, str]:
    """Simple heartbeat endpoint."""
    return {"message": "Welcome to CoffeeKing backend"}