from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase

from app.config import settings

is_sqlite = settings.sqlalchemy_url.startswith("sqlite")

connect_args = (
        {"check_same_thread": False} if is_sqlite else {"prepare_threshold": None}
)

pool_options = {} if is_sqlite else {"pool_size": 1, "max_overflow": 2, "pool_recycle": 300}

engine = create_engine(settings.sqlalchemy_url, connect_args=connect_args, pool_pre_ping=True, **pool_options)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    """Una sesion por request: se cierra sola al terminar."""
    with SessionLocal() as db:
        yield db