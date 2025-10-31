"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from . import auth, models
from .config import settings
from .database import Base, async_session_factory, engine
from .routers import auth as auth_router
from .routers import interviews as interviews_router
from .routers import users as users_router


app = FastAPI(title=settings.app_name, root_path=settings.root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    if settings.first_superuser_email and settings.first_superuser_password:
        async with async_session_factory() as session:
            stmt = select(models.User).where(
                models.User.email == settings.first_superuser_email.lower()
            )
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                super_user = models.User(
                    email=settings.first_superuser_email.lower(),
                    full_name="Auto Admin",
                    hashed_password=auth.get_password_hash(settings.first_superuser_password),
                    is_admin=True,
                )
                session.add(super_user)
                await session.commit()


@app.get("/health", response_model=dict[str, str])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(interviews_router.router)
