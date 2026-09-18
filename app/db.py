from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from app.config import settings

connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(
    settings.database_url, connect_args=connect_args, pool_pre_ping=True
)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    """Una sesion por request: se cierra sola al terminar."""
    with SessionLocal() as db:
        yield db
