"""Synthesizer agent — merges researcher findings into a report. (Phase 3 impl)"""

from __future__ import annotations

from typing import Any

from openscholar.agents.base import AgentResult, BaseAgent


class SynthesizerAgent(BaseAgent):
    name = "synthesizer"

    async def run(
        self, query: str, findings: list[dict[str, Any]], **_kwargs: Any
    ) -> AgentResult:
        # Phase 3: long-context Claude call combining all findings into markdown.
        return AgentResult(success=True, content="Report TBD in Phase 3")
