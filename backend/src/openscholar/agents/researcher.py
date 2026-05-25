"""Researcher agent — searches the web/papers for one sub-question. (Phase 2 impl)"""

from __future__ import annotations

from typing import Any

from openscholar.agents.base import AgentResult, BaseAgent


class ResearcherAgent(BaseAgent):
    name = "researcher"

    async def run(self, sub_question: str, **_kwargs: Any) -> AgentResult:
        # Phase 2: call Tavily/arXiv + Claude to extract facts.
        return AgentResult(
            success=True,
            content={"sub_question": sub_question, "findings": [], "sources": []},
        )
