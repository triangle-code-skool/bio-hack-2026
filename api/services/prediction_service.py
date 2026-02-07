from abc import ABC, abstractmethod
from typing import List, Dict

from schemas.prediction import PredictionRequest, PredictionResponse


class IPredictionService(ABC):
    """Interface for prediction services (Interface Segregation Principle)."""
    
    @abstractmethod
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """Generate viability prediction for an organ."""
        pass


class PredictionService(IPredictionService):
    """
    Service handling organ viability prediction business logic.
    Follows Single Responsibility Principle - only handles prediction logic.
    """
    
    def __init__(self):
        # Model will be loaded here in the future
        self._model = None
    
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Generate viability prediction for an organ.
        
        Args:
            request: PredictionRequest containing organ assessment data
            
        Returns:
            PredictionResponse with viability score and classification
        """
        # TODO: Replace with actual model inference
        score = self._calculate_mock_score(request)
        classification = self._get_classification(score)
        risk_factors = self._identify_risk_factors(request)
        feature_contributions = self._get_feature_contributions(request)
        
        return PredictionResponse(
            viability_score=score,
            classification=classification,
            confidence=0.85,
            risk_factors=risk_factors,
            feature_contributions=feature_contributions
        )
    
    def _calculate_mock_score(self, request: PredictionRequest) -> int:
        """Calculate mock viability score (placeholder for ML model)."""
        return 75
    
    def _get_classification(self, score: int) -> str:
        """Determine classification based on viability score."""
        if score < 40:
            return "Decline"
        elif score < 70:
            return "Marginal"
        return "Accept"
    
    def _identify_risk_factors(self, request: PredictionRequest) -> List[str]:
        """Identify risk factors from request data."""
        risk_factors = []
        
        if request.cold_ischemia_hours > 24:
            risk_factors.append("Extended cold ischemia time")
        if request.donor_age > 65:
            risk_factors.append("Advanced donor age")
        if request.warm_ischemia_minutes > 45:
            risk_factors.append("Extended warm ischemia time")
        if request.tissue_stiffness_kpa > 15:
            risk_factors.append("Elevated tissue stiffness")
            
        if not risk_factors:
            risk_factors.append("No significant risk factors identified")
            
        return risk_factors
    
    def _get_feature_contributions(self, request: PredictionRequest) -> Dict[str, float]:
        """Calculate feature contributions to prediction."""
        return {
            "stiffness": 0.4,
            "cold_ischemia": 0.3,
            "perfusion": 0.15,
            "donor_factors": 0.15
        }
