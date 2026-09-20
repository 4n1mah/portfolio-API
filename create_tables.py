"""Crea las tablas en la base de datos de DATABASE_URL. Se corre a mano, una sola vez por base."""

import app.models  # noqa: F401  (al importarlo, la tabla queda registrada en Base.metadata)
from app.db import Base, engine

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tablas listas en", engine.url.render_as_string(hide_password=True))
