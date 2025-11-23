from abc import ABC, abstractmethod
from typing import Protocol
from Core.Domain.domain_entities import AuditResult
from typing_extensions import runtime_checkable


@runtime_checkable
class ILLMAnalyzer(Protocol):
    """Interface for LLM-based audit analysis."""

    async def analyze(self, transcript: str) -> AuditResult:
        """Analyze a transcript and return an audit result.

        Args:
            transcript (str): The transcript to analyze

        Returns:
            AuditResult: The result of the audit analysis
        """
        ...