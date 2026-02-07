"""
Dependency injection utilities.
Follows Dependency Inversion Principle - high-level modules depend on abstractions.
"""
from functools import lru_cache

from services.prediction_service import PredictionService, IPredictionService


@lru_cache()
def get_prediction_service() -> IPredictionService:
    """
    Dependency injection for PredictionService.
    Uses caching to maintain singleton instance.
    
    Returns:
        IPredictionService implementation
    """
    return PredictionService()
