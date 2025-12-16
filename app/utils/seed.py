import json
from pathlib import Path
from typing import Iterable

from sqlalchemy.orm import Session

from app.models.core import Menu


DATA_PATH = Path(__file__).parent.parent.parent / "data" / "menus_seed.json"


def seed_menus(db: Session) -> int:
    if db.query(Menu).count() > 0:
        return 0

    if not DATA_PATH.exists():
        return 0

    with DATA_PATH.open("r", encoding="utf-8") as f:
        payload: Iterable[dict] = json.load(f)

    menus = [Menu(**item) for item in payload]
    db.add_all(menus)
    db.commit()
    return len(menus)
