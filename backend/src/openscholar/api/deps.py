"""FastAPI dependencies."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from openscholar.core.database import get_db
from openscholar.core.security import decode_token
from openscholar.models.user import User
from openscholar.services.research_service import ResearchService
from openscholar.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)

DbDep = Annotated[AsyncSession, Depends(get_db)]


def get_user_service(db: DbDep) -> UserService:
    return UserService(db)


def get_research_service(db: DbDep) -> ResearchService:
    return ResearchService(db)


async def get_current_user(
    token: Annotated[str | None, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise JWTError("Missing subject")
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {exc}",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    return await user_service.by_id(user_id)
