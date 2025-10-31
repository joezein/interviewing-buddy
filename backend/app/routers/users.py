"""User management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, models, schemas
from ..database import get_session


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserRead)
async def read_current_user(
    current_user: models.User = Depends(auth.get_current_active_user),
):
    return current_user


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(
    session: AsyncSession = Depends(get_session),
    _: models.User = Depends(auth.get_current_admin_user),
):
    result = await session.execute(select(models.User).order_by(models.User.created_at))
    return result.scalars().all()


@router.patch("/{user_id}", response_model=schemas.UserRead)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate,
    session: AsyncSession = Depends(get_session),
    _: models.User = Depends(auth.get_current_admin_user),
):
    stmt = select(models.User).where(models.User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_admin is not None:
        user.is_admin = user_update.is_admin
    if user_update.password:
        user.hashed_password = auth.get_password_hash(user_update.password)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
