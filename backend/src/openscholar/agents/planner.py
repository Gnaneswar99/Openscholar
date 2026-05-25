"""Planner agent — decomposes a query into sub-questions. (Phase 2 impl)"""

from __future__ import annotations

from typing import Any

from openscholar.agents.base import AgentResult, BaseAgent


class PlannerAgent(BaseAgent):
    name = "planner"

    async def run(self, query: str, **_kwargs: Any) -> AgentResult:
        # Phase 2: call Claude with a planning prompt.
        # For Phase 1 we return a deterministic stub so the API is exercisable.
        sub_questions = [
            f"What is the background of: {query}?",
            f"What are the key facts about: {query}?",
            f"What are the recent developments around: {query}?",
        ]
        return AgentResult(success=True, content=sub_questions)
