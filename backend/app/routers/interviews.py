"""Interview workflow endpoints."""

from datetime import datetime, timezone
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, models, schemas
from ..database import get_session
from ..templates import TEMPLATES


router = APIRouter(prefix="/interviews", tags=["interviews"])


@router.get("/templates", response_model=list[schemas.InterviewTemplate])
async def list_templates() -> list[schemas.InterviewTemplate]:
    return [schemas.InterviewTemplate(**template) for template in TEMPLATES.values()]


@router.get("/templates/{template_id}", response_model=schemas.InterviewTemplate)
async def get_template(template_id: str) -> schemas.InterviewTemplate:
    template = TEMPLATES.get(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return schemas.InterviewTemplate(**template)


@router.post("/sessions", response_model=schemas.InterviewSessionDetail, status_code=201)
async def create_session(
    session_in: schemas.InterviewSessionCreate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    template = TEMPLATES.get(session_in.template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")

    interview_session = models.InterviewSession(
        candidate_name=session_in.candidate_name,
        candidate_email=session_in.candidate_email,
        role=session_in.role,
        template_id=session_in.template_id,
        owner_id=current_user.id,
    )
    session.add(interview_session)
    await session.flush()

    for step in sorted(template.get("steps", []), key=lambda s: s.get("order", 0)):
        session.add(
            models.InterviewStep(
                session_id=interview_session.id,
                template_step_id=step["id"],
                title=step["title"],
                summary=step.get("summary"),
                order=step.get("order", 0),
                prompts=step.get("prompts"),
                scoring_guidance=step.get("scoring_guidance"),
            )
        )

    await session.commit()
    await session.refresh(interview_session)
    return await _get_session_detail(session, interview_session.id)


@router.get("/sessions", response_model=schemas.PaginatedResponse)
async def list_sessions(
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_current_active_user),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    offset = (page - 1) * size
    stmt = select(models.InterviewSession).order_by(models.InterviewSession.created_at.desc())
    count_stmt = select(func.count(models.InterviewSession.id))

    if not current_user.is_admin:
        stmt = stmt.where(models.InterviewSession.owner_id == current_user.id)
        count_stmt = count_stmt.where(models.InterviewSession.owner_id == current_user.id)

    stmt = stmt.offset(offset).limit(size)
    result = await session.execute(stmt)
    items = result.scalars().all()

    total = await session.scalar(count_stmt)

    payload = [schemas.InterviewSessionBase.model_validate(item) for item in items]
    return schemas.PaginatedResponse(items=payload, total=total or 0, page=page, size=size)


@router.get("/sessions/{session_id}", response_model=schemas.InterviewSessionDetail)
async def get_session_detail(
    session_id: UUID,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    interview_session = await session.get(models.InterviewSession, session_id)
    if not interview_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if interview_session.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view this session")
    return await _get_session_detail(session, session_id)


@router.patch("/sessions/{session_id}", response_model=schemas.InterviewSessionDetail)
async def update_session(
    session_id: UUID,
    session_update: schemas.InterviewSessionUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    interview_session = await session.get(models.InterviewSession, session_id)
    if not interview_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if interview_session.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to modify this session")

    if session_update.status is not None:
        interview_session.status = session_update.status
    if session_update.notes_summary is not None:
        interview_session.notes_summary = session_update.notes_summary
    if session_update.overall_score is not None:
        interview_session.overall_score = session_update.overall_score

    session.add(interview_session)
    await session.commit()
    return await _get_session_detail(session, session_id)


@router.patch("/sessions/{session_id}/steps/{step_id}", response_model=schemas.InterviewStepBase)
async def update_step(
    session_id: UUID,
    step_id: UUID,
    step_update: schemas.InterviewStepUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User = Depends(auth.get_current_active_user),
):
    interview_session = await session.get(models.InterviewSession, session_id)
    if not interview_session:
        raise HTTPException(status_code=404, detail="Session not found")
    if interview_session.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to modify this session")

    interview_step = await session.get(models.InterviewStep, step_id)
    if not interview_step or interview_step.session_id != session_id:
        raise HTTPException(status_code=404, detail="Step not found")

    if step_update.notes is not None:
        interview_step.notes = step_update.notes
    if step_update.score is not None:
        interview_step.score = step_update.score
    if step_update.is_completed is not None:
        interview_step.is_completed = step_update.is_completed
        interview_step.completed_at = (
            datetime.now(timezone.utc) if step_update.is_completed else None
        )

    session.add(interview_step)
    await session.commit()
    await session.refresh(interview_step)
    return schemas.InterviewStepBase.model_validate(interview_step)


async def _get_session_detail(
    session: AsyncSession, session_id: UUID
) -> schemas.InterviewSessionDetail:
    interview_session = await session.get(models.InterviewSession, session_id)
    if not interview_session:
        raise HTTPException(status_code=404, detail="Session not found")

    await session.refresh(interview_session, attribute_names=["steps"])
    return schemas.InterviewSessionDetail.model_validate(interview_session)
