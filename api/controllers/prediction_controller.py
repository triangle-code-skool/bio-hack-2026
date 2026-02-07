"""
Prediction controller - handles prediction endpoints.
Follows Single Responsibility Principle - only handles HTTP layer concerns.
"""
from fastapi import APIRouter, Depends

from schemas.prediction import PredictionRequest, PredictionResponse
from services.prediction_service import IPredictionService
from utils.dependencies import get_prediction_service

router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("", response_model=PredictionResponse)
async def predict(
    request: PredictionRequest,
    prediction_service: IPredictionService = Depends(get_prediction_service)
) -> PredictionResponse:
    """
    Generate organ viability prediction.
    
    Args:
        request: Organ assessment data
        prediction_service: Injected prediction service
        
    Returns:
        Viability prediction with score, classification, and risk factors
    """
    return prediction_service.predict(request)
