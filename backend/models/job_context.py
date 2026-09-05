"""Job context database model."""

from core.database import Base
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import TimestampMixin


class JobContext(Base, TimestampMixin):
    __tablename__ = "job_contexts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    target_role: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    company_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    job_description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Relationship back to User
    user = relationship(
        "User",
        back_populates="job_contexts",
    )

    competencies = relationship(
        "Competency",
        back_populates="job_context",
        cascade="all, delete-orphan",
    )
