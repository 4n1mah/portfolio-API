from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Visit(Base):
    """Una sección abierta por una sesión del navegador. La misma sesión cuenta una sola vez por sección."""

    __tablename__ = "visits"
    __table_args__ = (UniqueConstraint("session_id", "section"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    section: Mapped[str] = mapped_column(String(20), index=True)
    session_id: Mapped[str] = mapped_column(String(36))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
