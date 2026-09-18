from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db import Base, engine
from app.routers import visits


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas que falten al arrancar. Más adelante esto lo harán las migraciones (Alembic).
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
    return {"status": "ok"}
