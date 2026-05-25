"""Multi-agent system — Planner, Researcher, Synthesizer, Critic, Editor.

Phase 1 ships skeletons + interfaces. Phase 2 implements the single-agent MVP.
Phase 3 wires the full LangGraph pipeline.
"""

from openscholar.agents.base import AgentResult, BaseAgent

__all__ = ["AgentResult", "BaseAgent"]
