"""Monitoring and metrics collection"""

from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import os
from typing import Dict, Any

from ..utils.logger import get_logger

logger = get_logger(__name__)


# Define metrics
trip_requests_total = Counter(
    'timbuktoo_trip_requests_total',
    'Total number of trip requests',
    ['city', 'variant']
)

agent_calls_total = Counter(
    'timbuktoo_agent_calls_total',
    'Total number of agent calls',
    ['agent_type']
)

agent_costs = Summary(
    'timbuktoo_agent_costs_usd',
    'Agent costs in USD',
    ['agent_type']
)

agent_latency = Histogram(
    'timbuktoo_agent_latency_seconds',
    'Agent processing latency',
    ['agent_type'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0]
)

vector_search_latency = Histogram(
    'timbuktoo_vector_search_latency_seconds',
    'Vector search latency',
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

feedback_ratings = Histogram(
    'timbuktoo_feedback_ratings',
    'User feedback ratings',
    ['rating_type', 'variant'],
    buckets=[1, 2, 3, 4, 5]
)

active_trips = Gauge(
    'timbuktoo_active_trips',
    'Number of active trips being processed'
)

database_connections = Gauge(
    'timbuktoo_database_connections',
    'Number of active database connections',
    ['db_type']
)

trip_cost_total = Summary(
    'timbuktoo_trip_cost_usd',
    'Total trip cost in USD',
    ['variant']
)


class MetricsCollector:
    """Collects and exposes Prometheus metrics"""

    def __init__(self, port: int = 9090):
        self.port = port
        self.enabled = os.getenv("ENABLE_PROMETHEUS", "true").lower() == "true"

    def start(self):
        """Start Prometheus metrics server"""
        if self.enabled:
            try:
                start_http_server(self.port)
                logger.info(f"Prometheus metrics server started on port {self.port}")
            except Exception as e:
                logger.error(f"Failed to start Prometheus server: {str(e)}")

    def record_trip_request(self, city: str, variant: str):
        """Record a trip request"""
        if self.enabled:
            trip_requests_total.labels(city=city, variant=variant).inc()

    def record_agent_call(self, agent_type: str, cost_usd: float, latency_seconds: float):
        """Record an agent call"""
        if self.enabled:
            agent_calls_total.labels(agent_type=agent_type).inc()
            agent_costs.labels(agent_type=agent_type).observe(cost_usd)
            agent_latency.labels(agent_type=agent_type).observe(latency_seconds)

    def record_vector_search(self, latency_seconds: float):
        """Record vector search operation"""
        if self.enabled:
            vector_search_latency.observe(latency_seconds)

    def record_feedback(self, rating_type: str, rating: int, variant: str):
        """Record user feedback"""
        if self.enabled:
            feedback_ratings.labels(rating_type=rating_type, variant=variant).observe(rating)

    def record_trip_cost(self, cost_usd: float, variant: str):
        """Record total trip cost"""
        if self.enabled:
            trip_cost_total.labels(variant=variant).observe(cost_usd)

    def set_active_trips(self, count: int):
        """Set number of active trips"""
        if self.enabled:
            active_trips.set(count)

    def set_database_connections(self, db_type: str, count: int):
        """Set number of database connections"""
        if self.enabled:
            database_connections.labels(db_type=db_type).set(count)


# Singleton instance
_metrics_collector = None

def get_metrics_collector() -> MetricsCollector:
    """Get or create metrics collector instance"""
    global _metrics_collector
    if _metrics_collector is None:
        port = int(os.getenv("PROMETHEUS_PORT", "9090"))
        _metrics_collector = MetricsCollector(port=port)
    return _metrics_collector
