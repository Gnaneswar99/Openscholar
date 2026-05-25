"""Abstract agent interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    """Standard envelope returned by every agent run."""

    success: bool
    content: str | dict[str, Any] | list[Any]
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None


class BaseAgent(ABC):
    name: str = "base"

    @abstractmethod
    async def run(self, **kwargs: Any) -> AgentResult: ...
