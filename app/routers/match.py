from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Match, Table
from app.schemas.base import MatchCreate, MatchOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return db.query(Match).all()


@router.post("/", response_model=MatchOut, status_code=status.HTTP_201_CREATED)
def create_match(payload: MatchCreate, db: Session = Depends(get_db)):
    table = db.query(Table).get(payload.table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")

    match = Match(host_id=payload.host_id, table_id=payload.table_id, status="open")
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.post("/{match_id}/join", response_model=MatchOut)
def join_match(match_id: int, guest_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    if match.guest_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Match already filled")

    match.guest_id = guest_id
    match.status = "matched"
    db.commit()
    db.refresh(match)
    return match
