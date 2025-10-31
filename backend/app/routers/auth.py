"""Authentication endpoints."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import auth, models, schemas
from ..config import settings
from ..database import get_session


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await auth.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = auth.create_access_token(user.id, access_token_expires)
    return schemas.Token(access_token=token)


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: schemas.UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: models.User | None = Depends(auth.get_optional_user),
):
    # Allow open registration only if there are no users yet
    stmt = select(models.User)
    result = await session.execute(stmt)
    any_user = result.scalar_one_or_none()

    if any_user and (current_user is None or not current_user.is_admin):
        raise HTTPException(status_code=403, detail="Admin privileges required to create users")

    existing_user = await auth.get_user_by_email(session, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=user_in.email.lower(),
        full_name=user_in.full_name,
        hashed_password=auth.get_password_hash(user_in.password),
        is_admin=user_in.is_admin if any_user else True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
