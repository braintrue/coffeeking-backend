from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Table
from app.schemas.base import TableCreate, TableOut

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("/", response_model=list[TableOut])
def list_tables(db: Session = Depends(get_db)):
    return db.query(Table).all()


@router.post("/", response_model=TableOut, status_code=status.HTTP_201_CREATED)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    table = Table(**payload.dict())
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.patch("/{table_id}", response_model=TableOut)
def update_status(table_id: int, status: str, db: Session = Depends(get_db)):
    table = db.query(Table).get(table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    table.status = status
    db.commit()
    db.refresh(table)
    return table
