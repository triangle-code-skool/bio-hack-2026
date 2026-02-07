from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="UltraViab API", description="Organ Viability Assessment API")

class PredictionRequest(BaseModel):
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
    viability_score: int
    classification: str
    confidence: float
    risk_factors: List[str]
    feature_contributions: dict

@app.get("/")
async def root():
    return {"message": "UltraViab API is running"}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    # Mock prediction logic for now
    # This will be replaced with actual model inference later
    
    score = 75  # Default mock score
    classification = "Accept"
    if score < 40:
        classification = "Decline"
    elif score < 70:
        classification = "Marginal"
        
    return {
        "viability_score": score,
        "classification": classification,
        "confidence": 0.85,
        "risk_factors": ["Example risk factor"],
        "feature_contributions": {"stiffness": 0.4, "cit": 0.3}
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
