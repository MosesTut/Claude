"""Cost control utilities"""

from typing import Dict, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CostController:
    """Controls and monitors API costs"""

    def __init__(self, max_trip_cost_usd: float = 0.80):
        self.max_trip_cost_usd = max_trip_cost_usd
        self.current_trip_cost = 0.0
        self.agent_costs = {}

    def add_cost(self, agent_type: str, cost_usd: float) -> bool:
        """Add cost and check if within limits"""
        self.current_trip_cost += cost_usd

        if agent_type not in self.agent_costs:
            self.agent_costs[agent_type] = 0.0
        self.agent_costs[agent_type] += cost_usd

        if self.current_trip_cost > self.max_trip_cost_usd:
            logger.warning(
                "Trip cost limit exceeded",
                extra={
                    "current_cost": self.current_trip_cost,
                    "limit": self.max_trip_cost_usd,
                    "agent_costs": self.agent_costs
                }
            )
            return False
        return True

    def get_remaining_budget(self) -> float:
        """Get remaining budget"""
        return max(0, self.max_trip_cost_usd - self.current_trip_cost)

    def get_summary(self) -> Dict[str, Any]:
        """Get cost summary"""
        return {
            "total_cost_usd": round(self.current_trip_cost, 6),
            "max_cost_usd": self.max_trip_cost_usd,
            "remaining_budget_usd": round(self.get_remaining_budget(), 6),
            "agent_breakdown": {
                agent: round(cost, 6)
                for agent, cost in self.agent_costs.items()
            },
            "budget_utilized_pct": round(
                (self.current_trip_cost / self.max_trip_cost_usd) * 100, 2
            )
        }

    def can_afford(self, estimated_cost: float) -> bool:
        """Check if we can afford an operation"""
        return (self.current_trip_cost + estimated_cost) <= self.max_trip_cost_usd

    def degrade_gracefully(self) -> Dict[str, Any]:
        """Return degradation strategy when budget is low"""
        remaining = self.get_remaining_budget()

        if remaining < 0.10:
            return {
                "strategy": "minimal",
                "vector_chunks": 10,
                "max_tokens": 15000,
                "skip_tools": True
            }
        elif remaining < 0.30:
            return {
                "strategy": "reduced",
                "vector_chunks": 20,
                "max_tokens": 25000,
                "skip_tools": False
            }
        else:
            return {
                "strategy": "normal",
                "vector_chunks": 35,
                "max_tokens": 38000,
                "skip_tools": False
            }
