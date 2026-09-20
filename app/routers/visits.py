from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Visit
from app.schemas import SECTIONS, SectionStat, StatsOut, VisitIn

router = APIRouter(prefix="/visits", tags=["visits"])

DbSession = Annotated[Session, Depends(get_db)]
STATS_CACHE_SECONDS = 30

def require_known_origin(origin: Annotated[str | None, Header()] = None) -> None:
    """CORS solo lo obedece el navegador; esto mira de dónde viene la petición en el servidor.

    No es un candado: quien use curl puede mandar la cabecera que quiera. Lo que corta es a
    quien ve la petición en las herramientas del navegador y prueba a repetirla.
    """
    if origin not in settings.origins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Origen no permitido") 

@router.post("", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_known_origin)],)
def record_visit(visit: VisitIn, db: DbSession) -> None:
    db.add(Visit(section=visit.section, session_id=str(visit.session_id)))
    try:
        db.commit()
    except IntegrityError:
        # Esta sesión ya había abierto la sección: no se cuenta otra vez.
        db.rollback()
        
        
@router.get("/stats")
def get_stats(
    db: DbSession,
    response: Response,
    days: Annotated[int | None, Query(ge=1, le=365, description="Contar solo los últimos N días")] = None,
) -> StatsOut:
    query = select(Visit.section, func.count()).group_by(Visit.section)
    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        query = query.where(Visit.created_at >= cutoff)

    counts: dict[str, int] = dict(db.execute(query).all())
    sections = sorted(
        (SectionStat(section=s, visits=counts.get(s, 0)) for s in SECTIONS),
        key=lambda stat: stat.visits,
        reverse=True,
    )
    response.headers["Cache-Control"] = f"public, max-age={STATS_CACHE_SECONDS}"
    return StatsOut(
        total=sum(counts.values()),
        sections=sections,
        days=days,
        generated_at=datetime.now(timezone.utc),
    )