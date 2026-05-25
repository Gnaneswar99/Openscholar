"""Shared pytest fixtures."""

from __future__ import annotations

import asyncio
import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")

from httpx import ASGITransport, AsyncClient  # noqa: E402

from openscholar.core.database import AsyncSessionLocal, init_db  # noqa: E402
from openscholar.main import app  # noqa: E402


@pytest.fixture(scope="session")
def event_loop() -> Any:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[Any, None]:
    await init_db()
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: Any) -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient) -> AsyncClient:
    """Authenticated client — registers + logs in a test user."""
    await client.post(
        "/api/auth/register",
        json={
            "email": "tester@example.com",
            "password": "testpassword123",
            "full_name": "Test User",
        },
    )
    resp = await client.post(
        "/api/auth/login",
        json={"email": "tester@example.com", "password": "testpassword123"},
    )
    token = resp.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
