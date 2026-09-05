"""Competency database model."""

from core.database import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import TimestampMixin


class Competency(Base, TimestampMixin):
    __tablename__ = "competencies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    job_context_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("job_contexts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    importance: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    job_context = relationship(
        "JobContext",
        back_populates="competencies",
    )
