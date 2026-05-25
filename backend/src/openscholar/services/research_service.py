"""Research job service — CRUD and lifecycle.

The actual multi-agent execution lands in Phase 2. For Phase 1 we expose:
- Create a job (status = PENDING)
- List jobs for a user
- Read job + sources
- Update status (will be called by the orchestrator later)
"""

from __future__ import annotations

import logging

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from openscholar.core.exceptions import NotFoundError
from openscholar.models.research_job import ResearchJob, ResearchJobStatus

logger = logging.getLogger(__name__)


class ResearchService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user_id: str, query: str) -> ResearchJob:
        job = ResearchJob(
            user_id=user_id,
            query=query,
            status=ResearchJobStatus.PENDING,
        )
        self.session.add(job)
        await self.session.commit()
        await self.session.refresh(job)
        logger.info("Created research job %s for user %s", job.id, user_id)
        return job

    async def get(self, job_id: str, user_id: str | None = None) -> ResearchJob:
        stmt = select(ResearchJob).where(ResearchJob.id == job_id)
        if user_id is not None:
            stmt = stmt.where(ResearchJob.user_id == user_id)
        job = (await self.session.execute(stmt)).scalar_one_or_none()
        if not job:
            raise NotFoundError("Research job not found.")
        return job

    async def list_for_user(
        self, user_id: str, limit: int = 50, offset: int = 0
    ) -> tuple[list[ResearchJob], int]:
        total_stmt = (
            select(func.count())
            .select_from(ResearchJob)
            .where(ResearchJob.user_id == user_id)
        )
        total = (await self.session.execute(total_stmt)).scalar_one()

        stmt = (
            select(ResearchJob)
            .where(ResearchJob.user_id == user_id)
            .order_by(desc(ResearchJob.created_at))
            .limit(limit)
            .offset(offset)
        )
        rows = (await self.session.execute(stmt)).scalars().all()
        return list(rows), total

    async def update_status(
        self, job_id: str, status: ResearchJobStatus
    ) -> ResearchJob:
        job = await self.get(job_id)
        job.status = status
        await self.session.commit()
        await self.session.refresh(job)
        return job

    async def delete(self, job_id: str, user_id: str) -> None:
        job = await self.get(job_id, user_id=user_id)
        await self.session.delete(job)
        await self.session.commit()
