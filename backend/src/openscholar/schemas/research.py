"""Research job schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from openscholar.models.research_job import ResearchJobStatus


class SourceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    url: str
    snippet: str | None
    source_type: str
    relevance: float


class ResearchJobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    query: str
    title: str | None
    status: ResearchJobStatus
    created_at: datetime
    updated_at: datetime


class ResearchJobDetail(ResearchJobRead):
    sub_questions: list[str] | None = None
    report: str | None = None
    executive_summary: str | None = None
    faithfulness_score: float | None = None
    relevance_score: float | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    error_message: str | None = None
    sources: list[SourceRead] = []


class ResearchJobList(BaseModel):
    items: list[ResearchJobRead]
    total: int


class CreateResearchJobRequest(BaseModel):
    query: str = Field(min_length=10, max_length=2000)
