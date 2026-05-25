"""Critic agent — scores faithfulness + flags weak citations. (Phase 6 impl)"""

from __future__ import annotations

from typing import Any

from openscholar.agents.base import AgentResult, BaseAgent


class CriticAgent(BaseAgent):
    name = "critic"

    async def run(
        self, report: str, sources: list[dict[str, Any]], **_kwargs: Any
    ) -> AgentResult:
        # Phase 6: RAGAS-style faithfulness + relevance scoring.
        return AgentResult(
            success=True,
            content={"faithfulness": 0.0, "relevance": 0.0, "issues": []},
        )
