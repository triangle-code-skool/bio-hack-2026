from pydantic import BaseModel
from typing import List, Optional


class PredictionRequest(BaseModel):
    """Request model for organ viability prediction."""
    organ_type: str
    tissue_stiffness_kpa: float
    resistive_index: float
    shear_wave_velocity_ms: float
    perfusion_uniformity_pct: float
    echogenicity_grade: int
    edema_index: int
    cold_ischemia_hours: float
    donor_age: int
    kdpi_percentile: Optional[int] = None
    cause_of_death: str
    warm_ischemia_minutes: float


class PredictionResponse(BaseModel):
    """Response model for organ viability prediction."""
    viability_score: int
    classification: str
    confidence: float
    risk_factors: List[str]
    feature_contributions: dict
