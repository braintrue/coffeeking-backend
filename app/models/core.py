from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")
    hosted_matches = relationship("Match", foreign_keys="Match.host_id", back_populates="host")
    guest_matches = relationship("Match", foreign_keys="Match.guest_id", back_populates="guest")


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    order_items = relationship("OrderItem", back_populates="menu")


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    capacity = Column(Integer, default=2)
    status = Column(String, default="available")
    location_code = Column(String, nullable=False, index=True)
    tagline = Column(String, nullable=True)
    current_count = Column(Integer, nullable=False, default=0)

    orders = relationship("Order", back_populates="table")
    matches = relationship("Match", back_populates="table")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    status = Column(String, default="pending")
    total_amount = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    table = relationship("Table", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    quantity = Column(Integer, default=1)

    order = relationship("Order", back_populates="items")
    menu = relationship("Menu", back_populates="order_items")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    status = Column(String, default="open")
    created_at = Column(DateTime, default=datetime.utcnow)

    host = relationship("User", foreign_keys=[host_id], back_populates="hosted_matches")
    guest = relationship("User", foreign_keys=[guest_id], back_populates="guest_matches")
    table = relationship("Table", back_populates="matches")
