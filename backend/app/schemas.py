"""Pydantic schemas for API responses and requests."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_encoders={Decimal: float})


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None


class UserBase(ORMBaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(ORMBaseModel):
    email: EmailStr
    full_name: str | None = None
    password: str = Field(min_length=8)
    is_admin: bool = False


class UserUpdate(ORMBaseModel):
    full_name: str | None = None
    password: str | None = Field(default=None, min_length=8)
    is_active: bool | None = None
    is_admin: bool | None = None


class UserRead(UserBase):
    id: UUID
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime


class InterviewTemplateStep(ORMBaseModel):
    id: str
    title: str
    summary: str | None = None
    prompts: dict[str, Any] | None = None
    scoring_guidance: dict[str, Any] | None = None
    order: int


class InterviewTemplate(ORMBaseModel):
    id: str
    title: str
    description: str
    tags: list[str] = []
    phases: list[dict[str, Any]]
    weightings: list[dict[str, Any]]


class InterviewStepBase(ORMBaseModel):
    id: UUID
    template_step_id: str
    title: str
    summary: str | None
    prompts: dict[str, Any] | None
    scoring_guidance: dict[str, Any] | None
    order: int
    notes: str | None
    score: float | None
    is_completed: bool
    updated_at: datetime

class InterviewStepUpdate(ORMBaseModel):
    notes: str | None = None
    score: float | None = Field(default=None, ge=0, le=5)
    is_completed: bool | None = None


class InterviewSessionBase(ORMBaseModel):
    id: UUID
    candidate_name: str
    candidate_email: str | None
    role: str
    template_id: str
    status: str
    notes_summary: str | None
    overall_score: float | None
    created_at: datetime
    updated_at: datetime

class InterviewSessionCreate(ORMBaseModel):
    candidate_name: str
    candidate_email: str | None = None
    role: str
    template_id: str


class InterviewSessionUpdate(ORMBaseModel):
    status: str | None = None
    notes_summary: str | None = None
    overall_score: float | None = Field(default=None, ge=0, le=5)


class InterviewSessionDetail(InterviewSessionBase):
    steps: list[InterviewStepBase]


class PaginatedResponse(ORMBaseModel):
    items: list[Any]
    total: int
    page: int
    size: int
