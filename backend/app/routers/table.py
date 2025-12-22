"""Endpoints for managing tables within the coffee shop."""

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Table
from app.schemas.base import TableCreate, TableOut


router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("/", response_model=list[TableOut])
def list_tables(db: Session = Depends(get_db)):
    """Return all tables."""
    return db.query(Table).all()


@router.post("/", response_model=TableOut, status_code=status.HTTP_201_CREATED)
def create_table(payload: TableCreate, db: Session = Depends(get_db)):
    """Create a new table."""
    table = Table(**payload.dict())
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.get("/{table_id}", response_model=TableOut)
def get_table(table_id: int, db: Session = Depends(get_db)):
    """Return a specific table by ID."""
    table = db.query(Table).get(table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    return table


@router.patch("/{table_id}", response_model=TableOut)
def update_status(table_id: int, status: str, db: Session = Depends(get_db)):
    """Update the status of a table (e.g., available, occupied)."""
    table = db.query(Table).get(table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    table.status = status
    db.commit()
    db.refresh(table)
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    """Delete a table by ID."""
    table = db.query(Table).get(table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    db.delete(table)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)