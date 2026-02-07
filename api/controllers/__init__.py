from .health_controller import router as health_router
from .prediction_controller import router as prediction_router

__all__ = ["health_router", "prediction_router"]
