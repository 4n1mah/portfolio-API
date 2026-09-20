from typing import Literal, get_args
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

Section = Literal["about", "portfolio", "skills", "experience"]
SECTIONS: tuple[Section, ...] = get_args(Section)


class VisitIn(BaseModel):
    section: Section
    session_id: UUID


class SectionStat(BaseModel):
    section: Section
    visits: int


class StatsOut(BaseModel):
    total: int
    sections: list[SectionStat]
    days: int | None = None
    generated_at: datetime
