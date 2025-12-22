"""Re-export all SQLAlchemy models from this package.

Importing from this module will pull in the individual classes defined in
``core.py``.  Keeping the exports here makes it easy to import models from
``app.models`` without referencing submodules.
"""

from app.models.core import Match, Menu, Order, OrderItem, Table, User

__all__ = [
    "User",
    "Menu",
    "Table",
    "Order",
    "OrderItem",
    "Match",
]