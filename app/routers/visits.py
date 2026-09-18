from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Visit
from app.schemas import SECTIONS, SectionStat, StatsOut, VisitIn

router = APIRouter(prefix="/visits", tags=["visits"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("", status_code=status.HTTP_204_NO_CONTENT)
def record_visit(visit: VisitIn, db: DbSession) -> None:
    db.add(Visit(section=visit.section, session_id=str(visit.session_id)))
    try:
        db.commit()
    except IntegrityError:
        # Esta sesión ya había abierto la sección: no se cuenta otra vez.
        db.rollback()


@router.get("/stats")
def get_stats(db: DbSession) -> StatsOut:
    rows = db.execute(select(Visit.section, func.count()).group_by(Visit.section)).all()
    counts: dict[str, int] = dict(rows)
    sections = sorted(
        (SectionStat(section=s, visits=counts.get(s, 0)) for s in SECTIONS),
        key=lambda stat: stat.visits,
        reverse=True,
    )
    return StatsOut(total=sum(counts.values()), sections=sections)
