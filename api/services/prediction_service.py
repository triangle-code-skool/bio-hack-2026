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
        # Weights from DEEP_RESEARCH.md
        self.weights = {
            "stiffness": 0.28,
            "resistive_index": 0.22,
            "perfusion_uniformity": 0.15,
            "echogenicity": 0.10,
            "edema_index": 0.05,
            "kdpi": 0.10,
            "cold_ischemia_time": 0.06,
            "donor_age": 0.03,
            "cause_of_death": 0.01
        }
    
    def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Generate viability prediction for an organ.
        
        Args:
            request: PredictionRequest containing organ assessment data
            
        Returns:
            PredictionResponse with viability score and classification
        """
        score = self._calculate_score(request)
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
    
    def _calculate_score(self, request: PredictionRequest) -> int:
        """Calculate viability score using weighted sum of normalized inputs."""
        
        # 1. Normalization (Min-Max Scaling)
        # Stiffness: 0-50 kPa (Lower is better -> Invert)
        norm_stiffness = 1.0 - min(max((request.tissue_stiffness_kpa - 0) / (50 - 0), 0), 1)
        
        # RI: 0.4-1.0 (Lower is better -> Invert)
        norm_ri = 1.0 - min(max((request.resistive_index - 0.4) / (1.0 - 0.4), 0), 1)
        
        # Perfusion Uniformity: 0-100% (Higher is better -> Direct)
        norm_perfusion = min(max((request.perfusion_uniformity_pct - 0) / (100 - 0), 0), 1)
        
        # Echogenicity: 1-5 (Lower is better -> Invert)
        norm_echo = 1.0 - min(max((request.echogenicity_grade - 1) / (5 - 1), 0), 1)
        
        # Edema Index: 0.39 threshold, assume range roughly 0.2 - 0.6 for normalization?
        # Doc says > 0.39 is bad. Let's assume 0.2 (dry) to 0.6 (very edematous).
        # Lower is better -> Invert
        norm_edema = 1.0 - min(max((request.edema_index - 0.2) / (0.6 - 0.2), 0), 1)
        
        # KDPI: 0-100% (Lower is better -> Invert)
        kdpi_val = request.kdpi_percentile if request.kdpi_percentile is not None else 50 # Default middle
        norm_kdpi = 1.0 - min(max((kdpi_val - 0) / (100 - 0), 0), 1)
        
        # CIT: 0-48 hours (Lower is better -> Invert)
        norm_cit = 1.0 - min(max((request.cold_ischemia_hours - 0) / (48 - 0), 0), 1)
        
        # Age: 0-90 years (Lower is better -> Invert)
        norm_age = 1.0 - min(max((request.donor_age - 0) / (90 - 0), 0), 1)
        
        # Cause of Death: 0.01 weight. No mapping logic provided. Assume nominal.
        # Let's say we give it 0.5 (neutral) for now as we can't parse string efficiently without a map.
        norm_cod = 0.5

        # 2. Weighted Sum
        raw_score = (
            norm_stiffness * self.weights["stiffness"] +
            norm_ri * self.weights["resistive_index"] +
            norm_perfusion * self.weights["perfusion_uniformity"] +
            norm_echo * self.weights["echogenicity"] +
            norm_edema * self.weights["edema_index"] +
            norm_kdpi * self.weights["kdpi"] +
            norm_cit * self.weights["cold_ischemia_time"] +
            norm_age * self.weights["donor_age"] +
            norm_cod * self.weights["cause_of_death"]
        )
        
        # Scale to 0-100
        return int(raw_score * 100)
    
    def _get_classification(self, score: int) -> str:
        """Determine classification based on viability score."""
        # Per doc: 0-39 Decline, 40-69 Marginal, 70-100 Accept
        if score < 40:
            return "Decline"
        if score < 70:
            return "Marginal"
        return "Accept"
    
    def _identify_risk_factors(self, request: PredictionRequest) -> List[str]:
        """Identify risk factors from request data."""
        risk_factors = []
        
        # Doc thresholds:
        # PCL: RI > 0.8 is pathological.
        if request.resistive_index > 0.8:
            risk_factors.append("High Vascular Resistance (RI > 0.8)")
            
        # Stiffness: > 28 kPa (Kidney) is dysfunctional.
        if request.tissue_stiffness_kpa > 28.0:
            risk_factors.append("Critical Tissue Stiffness (> 28 kPa)")
            
        # Edema: Index > 0.39
        if request.edema_index > 0.39:
            risk_factors.append("Significant Edema (> 0.39)")

        if request.cold_ischemia_hours > 24:
            risk_factors.append("Extended Cold Ischemia (> 24h)")
            
        if request.donor_age > 60:
             risk_factors.append("Advanced Donor Age (> 60)")
            
        if not risk_factors:
            risk_factors.append("No significant risk factors identified")
            
        return risk_factors
    
    def _get_feature_contributions(self, request: PredictionRequest) -> Dict[str, float]:
        """Calculate feature contributions to prediction."""
        return {
            "stiffness": self.weights["stiffness"],
            "resistive_index": self.weights["resistive_index"],
            "perfusion_uniformity": self.weights["perfusion_uniformity"],
            "echogenicity": self.weights["echogenicity"],
            "edema_index": self.weights["edema_index"],
            "kdpi": self.weights["kdpi"],
            "cold_ischemia_time": self.weights["cold_ischemia_time"],
            "donor_age": self.weights["donor_age"],
            "cause_of_death": self.weights["cause_of_death"]
        }
