from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Table
from app.schemas.base import TableCreate, TableOut
from app.routers.auth import get_current_user


class TableJoinResponse(BaseModel):
    table: TableOut
    message: Optional[str] = None

router = APIRouter(prefix="/tables", tags=["tables"])


@router.get("/", response_model=list[TableOut])
def list_tables(
    location_code: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    query = db.query(Table)
    if location_code:
        query = query.filter(Table.location_code == location_code)
    return query.all()


@router.post("/", response_model=TableOut, status_code=status.HTTP_201_CREATED)
def create_table(payload: TableCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    table = Table(
        name=payload.name,
        capacity=payload.capacity,
        tagline=payload.tagline,
        location_code=payload.location_code,
        status="available",
        current_count=1,
    )
    db.add(table)
    db.commit()
    db.refresh(table)
    return table


@router.post("/{table_id}/join", response_model=TableJoinResponse)
def join_table(table_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    table = db.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")

    table.current_count += 1
    message: Optional[str] = None

    if table.current_count >= table.capacity:
        table.status = "matched"
        message = f"{table.id}번 테이블로 가세요"

    db.commit()
    db.refresh(table)

    return TableJoinResponse(table=table, message=message)
