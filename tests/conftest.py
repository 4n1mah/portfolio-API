import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

@pytest.fixture
def db_engine():
    """Una base de datos SQLite en memoria, nueva en cada test."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db(db_engine):
    """Sesion directa a esa misma base, para preparar datos antes de llamar a la API"""
    with Session(db_engine) as session:
        yield session
        
@pytest.fixture
def client(db_engine):
    """Cliente de pruebas conectado a la base de datos del test"""
    TestingSession = sessionmaker(bind=db_engine)

    def override_get_db():
        with TestingSession() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()