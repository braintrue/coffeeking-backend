from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Menu, Order, OrderItem
from app.schemas.base import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()


@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order requires items")

    order = Order(user_id=1, table_id=payload.table_id, status="pending")
    db.add(order)
    db.flush()

    total_amount = 0
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
