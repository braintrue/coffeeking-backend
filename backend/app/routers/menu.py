"""Endpoints for managing coffee menu items."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Menu
from app.schemas.base import MenuCreate, MenuOut, MenuUpdate


router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=list[MenuOut])
def list_menus(db: Session = Depends(get_db)):
    """Return all menu items."""
    return db.query(Menu).all()


@router.post("/", response_model=MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuCreate, db: Session = Depends(get_db)):
    """Create a new menu item."""
    menu = Menu(**payload.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.get("/{menu_id}", response_model=MenuOut)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    """Return a single menu item by ID."""
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return menu


@router.patch("/{menu_id}", response_model=MenuOut)
def update_menu(menu_id: int, payload: MenuUpdate, db: Session = Depends(get_db)):
    """Partially update a menu item.  Only provided fields are modified."""
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    update_data = payload.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(menu, field, value)
    db.commit()
    db.refresh(menu)
    return menu


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    """Delete a menu item by ID."""
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    db.delete(menu)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)