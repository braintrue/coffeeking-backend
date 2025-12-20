"""Database utilities for the CoffeeKing backend.

This module defines the SQLAlchemy engine, declarative base and session
factories used throughout the application.  It also provides helpers for
dependency injection within FastAPI and a context manager for unit of work
style interactions.
"""

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings


settings = get_settings()

# Create the SQLAlchemy engine.  For SQLite we must pass
# ``check_same_thread=False`` so that the same connection can be shared across
# threads when used with TestClient.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
    if "sqlite" in settings.database_url
    else {},
)

# Session factory configured not to autocommit or autoflush.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base class for our models.
Base = declarative_base()


def get_db() -> Generator:
    """Yield a database session for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator:
    """Provide a transactional scope around a series of operations.

    This helper is useful for scripts or tasks where you want to ensure that
    either all operations succeed or none do.  It will automatically commit
    the session on success or roll back on exception.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()