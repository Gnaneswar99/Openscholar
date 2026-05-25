"""User auth + management."""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from openscholar.core.exceptions import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
)
from openscholar.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from openscholar.models.user import User, UserRole
from openscholar.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def register(self, payload: RegisterRequest) -> User:
        existing = await self._by_email(payload.email)
        if existing:
            raise ValidationError("A user with this email already exists.")

        # First registered user becomes admin
        count_stmt = select(User).limit(1)
        first_user = (await self.session.execute(count_stmt)).scalar_one_or_none()
        role = UserRole.USER if first_user else UserRole.ADMIN

        user = User(
            email=payload.email.lower(),
            hashed_password=hash_password(payload.password),
            full_name=payload.full_name,
            role=role,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        logger.info("Registered user %s role=%s", user.email, user.role.value)
        return user

    async def login(self, payload: LoginRequest) -> TokenResponse:
        user = await self._by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise AuthenticationError("Invalid credentials.")
        if not user.is_active:
            raise AuthenticationError("Account disabled.")

        return TokenResponse(
            access_token=create_access_token(user.id, {"role": user.role.value}),
            refresh_token=create_refresh_token(user.id),
        )

    async def by_id(self, user_id: str) -> User:
        stmt = select(User).where(User.id == user_id)
        user = (await self.session.execute(stmt)).scalar_one_or_none()
        if not user:
            raise NotFoundError("User not found.")
        return user

    async def _by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return (await self.session.execute(stmt)).scalar_one_or_none()
