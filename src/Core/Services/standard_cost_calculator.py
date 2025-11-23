from typing import Dict, Any
from Core.Domain.domain_entities import AuditResult


class StandardCostCalculator:
    """Calculate standard costs and metrics based on audit results."""

    def __init__(self):
        """Initialize the cost calculator."""
        pass

    def calculate_costs(self, audit_result: AuditResult) -> Dict[str, Any]:
        """Calculate standard costs based on audit result.

        Args:
            audit_result: The audit result to calculate costs for

        Returns:
            Dict containing cost calculations
        """
        base_cost = 1000.0
        risk_multiplier = 1.0 + (audit_result.risk_score * 0.5)
        recommendation_factor = len(audit_result.recommendations) * 100

        total_cost = base_cost * risk_multiplier + recommendation_factor

        return {
            'base_cost': base_cost,
            'risk_adjustment': base_cost * (risk_multiplier - 1.0),
            'recommendation_cost': recommendation_factor,
            'total_cost': total_cost,
            'cost_breakdown': {
                'risk_score': audit_result.risk_score,
                'num_risk_factors': len(audit_result.risk_factors),
                'num_recommendations': len(audit_result.recommendations)
            }
        }