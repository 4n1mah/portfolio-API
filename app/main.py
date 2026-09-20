from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers import visits


@asynccontextmanager
async def lifespan(app: FastAPI):
    # En local (SQLite) las tablas se crean al vuelo. En producción no: ya existen (create_tables.py),
    # y si la base fallara, el arranque tumbaría hasta /health.
    if settings.sqlalchemy_url.startswith("sqlite"):
        Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Portfolio API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.include_router(visits.router)


@app.get("/health")
def health() -> dict[str, str]:
    # El esquema (sqlite o postgresql+psycopg) dice qué base usa este despliegue, sin filtrar la URL.
    return {"status": "ok", "database": settings.sqlalchemy_url.split("://", 1)[0]}
