"""Research job CRUD tests."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_and_list_jobs(auth_client: AsyncClient) -> None:
    # Empty list initially
    resp = await auth_client.get("/api/research")
    assert resp.status_code == 200
    assert resp.json()["total"] == 0

    # Create a job
    resp = await auth_client.post(
        "/api/research",
        json={"query": "What are recent advances in vector databases for AI?"},
    )
    assert resp.status_code == 201
    job = resp.json()
    assert job["status"] == "pending"
    job_id = job["id"]

    # List shows it
    resp = await auth_client.get("/api/research")
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == job_id

    # Detail
    resp = await auth_client.get(f"/api/research/{job_id}")
    assert resp.status_code == 200
    assert resp.json()["query"].startswith("What are recent advances")


@pytest.mark.asyncio
async def test_create_validates_query_length(auth_client: AsyncClient) -> None:
    resp = await auth_client.post("/api/research", json={"query": "too short"})
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_research_requires_auth(client: AsyncClient) -> None:
    resp = await client.get("/api/research")
    assert resp.status_code == 401
