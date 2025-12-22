"""Endpoints for managing user matches on tables."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.core import Match, Table, User
from app.schemas.base import MatchCreate, MatchOut
from app.routers.auth import get_current_user


router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/", response_model=list[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    """Return all matches."""
    return db.query(Match).all()


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Return a match by ID."""
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return match


@router.post("/", response_model=MatchOut, status_code=status.HTTP_201_CREATED)
def create_match(
    payload: MatchCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MatchOut:
    """Create a new match for the authenticated host.

    The ``host_id`` from the payload is ignored in favour of the current user.
    A 404 is raised if the table does not exist.
    """
    table = db.query(Table).get(payload.table_id)
    if not table:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
    match = Match(host_id=current_user.id, table_id=payload.table_id, status="open")
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.post("/{match_id}/join", response_model=MatchOut)
def join_match(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> MatchOut:
    """Join an existing match as the guest.

    The guest is always set to the authenticated user.  A 404 error is raised
    if the match does not exist and a 400 error is raised if the match is
    already filled.
    """
    match = db.query(Match).get(match_id)
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    if match.guest_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Match already filled")
    match.guest_id = current_user.id
    match.status = "matched"
    db.commit()
    db.refresh(match)
    return match