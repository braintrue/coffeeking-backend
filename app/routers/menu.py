from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Menu
from app.schemas.base import MenuCreate, MenuOut

router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=list[MenuOut])
def list_menus(db: Session = Depends(get_db)):
    return db.query(Menu).all()


@router.post("/", response_model=MenuOut, status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuCreate, db: Session = Depends(get_db)):
    menu = Menu(**payload.dict())
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu


@router.get("/{menu_id}", response_model=MenuOut)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return menu
