"""Research job endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from openscholar.api.deps import get_current_user, get_research_service
from openscholar.core.exceptions import AppError
from openscholar.models.user import User
from openscholar.schemas.research import (
    CreateResearchJobRequest,
    ResearchJobDetail,
    ResearchJobList,
    ResearchJobRead,
    SourceRead,
)
from openscholar.services.research_service import ResearchService

router = APIRouter(prefix="/research", tags=["research"])


@router.post("", response_model=ResearchJobRead, status_code=status.HTTP_201_CREATED)
async def create_job(
    payload: CreateResearchJobRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResearchService, Depends(get_research_service)],
) -> ResearchJobRead:
    job = await service.create(user_id=user.id, query=payload.query)
    # Phase 2 will dispatch background task here:
    # background_tasks.add_task(run_research_pipeline, job.id)
    return ResearchJobRead.model_validate(job)


@router.get("", response_model=ResearchJobList)
async def list_jobs(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResearchService, Depends(get_research_service)],
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> ResearchJobList:
    items, total = await service.list_for_user(user.id, limit=limit, offset=offset)
    return ResearchJobList(
        items=[ResearchJobRead.model_validate(j) for j in items], total=total
    )


@router.get("/{job_id}", response_model=ResearchJobDetail)
async def get_job(
    job_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResearchService, Depends(get_research_service)],
) -> ResearchJobDetail:
    try:
        job = await service.get(job_id, user_id=user.id)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return ResearchJobDetail(
        id=job.id,
        query=job.query,
        title=job.title,
        status=job.status,
        sub_questions=job.sub_questions,
        report=job.report,
        executive_summary=job.executive_summary,
        faithfulness_score=job.faithfulness_score,
        relevance_score=job.relevance_score,
        tokens_in=job.tokens_in,
        tokens_out=job.tokens_out,
        cost_usd=job.cost_usd,
        error_message=job.error_message,
        created_at=job.created_at,
        updated_at=job.updated_at,
        sources=[SourceRead.model_validate(s) for s in job.sources],
    )


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: str,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ResearchService, Depends(get_research_service)],
) -> None:
    try:
        await service.delete(job_id, user_id=user.id)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
