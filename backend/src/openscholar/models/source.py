"""Source model — a citation discovered by a research agent."""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from openscholar.models.base import Base

if TYPE_CHECKING:
    from openscholar.models.research_job import ResearchJob


class Source(Base):
    """A single source / citation backing claims in a report."""

    __tablename__ = "sources"

    job_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("research_jobs.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String(1024))
    url: Mapped[str] = mapped_column(String(2048))
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 'web', 'arxiv', 'semantic_scholar', 'user_upload', etc.
    source_type: Mapped[str] = mapped_column(String(64), default="web")

    # Relevance score assigned by the researcher agent (0..1)
    relevance: Mapped[float] = mapped_column(Float, default=0.0)

    job: Mapped["ResearchJob"] = relationship(back_populates="sources")

    def __repr__(self) -> str:
        return f"<Source {self.title[:40]!r}>"
