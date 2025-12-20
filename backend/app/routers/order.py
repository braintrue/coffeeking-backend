"""Endpoints for creating and retrieving orders."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Menu, Order, OrderItem, User
from app.schemas.base import OrderCreate, OrderOut
from app.routers.auth import get_current_user


router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    """Return all orders."""
    return db.query(Order).all()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> OrderOut:
    """Create a new order for the currently authenticated user.

    The ``user_id`` field is not taken from the payload; instead the user
    information is derived from the JWT token.  A 400 error is raised if
    no items are provided and a 404 error is raised if any referenced menu
    item does not exist.
    """
    if not payload.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order requires items")

    order = Order(user_id=current_user.id, table_id=payload.table_id, status="pending")
    db.add(order)
    db.flush()  # get order.id before inserting items

    total_amount: float = 0.0
    for item in payload.items:
        menu = db.query(Menu).get(item.menu_id)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu {item.menu_id} not found")
        order_item = OrderItem(order_id=order.id, menu_id=item.menu_id, quantity=item.quantity)
        db.add(order_item)
        total_amount += menu.price * item.quantity

    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return order


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Retrieve a single order by its identifier."""
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order