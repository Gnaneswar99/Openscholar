"""Auth endpoints."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError

from openscholar.api.deps import get_current_user, get_user_service
from openscholar.core.exceptions import AppError
from openscholar.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from openscholar.models.user import User
from openscholar.schemas.auth import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from openscholar.schemas.user import UserRead
from openscholar.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    try:
        return await user_service.register(payload)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> TokenResponse:
    try:
        return await user_service.login(payload)
    except AppError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc


@router.post("/refresh", response_model=TokenResponse)
async def refresh(
    payload: RefreshRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> TokenResponse:
    try:
        token_data = decode_token(payload.refresh_token)
        if token_data.get("type") != "refresh":
            raise JWTError("Not a refresh token")
        user = await user_service.by_id(token_data["sub"])
    except (JWTError, AppError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        ) from exc

    return TokenResponse(
        access_token=create_access_token(user.id, {"role": user.role.value}),
        refresh_token=create_refresh_token(user.id),
    )


@router.get("/me", response_model=UserRead)
async def me(user: Annotated[User, Depends(get_current_user)]) -> User:
    return user
