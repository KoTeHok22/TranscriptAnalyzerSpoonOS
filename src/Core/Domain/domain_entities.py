from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AuditResult:
    """Represents the result of an audit analysis."""

    risk_score: float
    risk_factors: List[str]
    recommendations: List[str]
    summary: str
    confidence: float
    details: Optional[str] = None