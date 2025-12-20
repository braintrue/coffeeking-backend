"""SQLAlchemy model definitions for the CoffeeKing backend."""

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    """User accounts with email and hashed password."""

    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    full_name: str | None = Column(String, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    hosted_matches = relationship("Match", foreign_keys="Match.host_id", back_populates="host")
    guest_matches = relationship("Match", foreign_keys="Match.guest_id", back_populates="guest")


class Menu(Base):
    """Coffee menu items offered by CoffeeKing."""

    __tablename__ = "menus"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    description: str | None = Column(String, nullable=True)
    price: float = Column(Float, nullable=False)
    is_available: bool = Column(Boolean, default=True)

    order_items = relationship("OrderItem", back_populates="menu")


class Table(Base):
    """Physical tables available in the coffee shop for matching users."""

    __tablename__ = "tables"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, nullable=False)
    capacity: int = Column(Integer, default=2)
    status: str = Column(String, default="available")

    orders = relationship("Order", back_populates="table")
    matches = relationship("Match", back_populates="table")


class Order(Base):
    """Customer orders comprised of one or more menu items."""

    __tablename__ = "orders"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_id: int = Column(Integer, ForeignKey("tables.id"), nullable=False)
    status: str = Column(String, default="pending")
    total_amount: float = Column(Float, default=0)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Join table representing menu items within an order."""

    __tablename__ = "order_items"

    id: int = Column(Integer, primary_key=True, index=True)
    order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id: int = Column(Integer, ForeignKey("menus.id"), nullable=False)
    quantity: int = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    menu = relationship("Menu", back_populates="order_items")


class Match(Base):
    """Represents a pairing between a host and an optional guest at a table."""

    __tablename__ = "matches"

    id: int = Column(Integer, primary_key=True, index=True)
    host_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    guest_id: int | None = Column(Integer, ForeignKey("users.id"), nullable=True)
    table_id: int = Column(Integer, ForeignKey("tables.id"), nullable=False)
    status: str = Column(String, default="open")
    created_at: datetime = Column(DateTime, default=datetime.utcnow)

    host = relationship("User", foreign_keys=[host_id], back_populates="hosted_matches")
    guest = relationship("User", foreign_keys=[guest_id], back_populates="guest_matches")
    table = relationship("Table", back_populates="matches")