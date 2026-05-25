"""Research job — one query and its multi-agent execution."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from openscholar.models.base import Base

if TYPE_CHECKING:
    from openscholar.models.source import Source


class ResearchJobStatus(enum.StrEnum):
    PENDING = "pending"
    PLANNING = "planning"
    RESEARCHING = "researching"
    SYNTHESIZING = "synthesizing"
    CRITIQUING = "critiquing"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchJob(Base):
    """One research query and its full execution state."""

    __tablename__ = "research_jobs"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    query: Mapped[str] = mapped_column(Text)
    title: Mapped[str | None] = mapped_column(String(512), nullable=True)
    status: Mapped[ResearchJobStatus] = mapped_column(
        Enum(ResearchJobStatus), default=ResearchJobStatus.PENDING, index=True
    )

    # Sub-questions decided by the planner (json list of strings)
    sub_questions: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)

    # Final report markdown
    report: Mapped[str | None] = mapped_column(Text, nullable=True)
    executive_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Evaluation
    faithfulness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    relevance_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Cost tracking
    tokens_in: Mapped[int] = mapped_column(Integer, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, default=0)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.0)

    # Error tracking
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    sources: Mapped[list[Source]] = relationship(
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<ResearchJob {self.id} status={self.status.value}>"
