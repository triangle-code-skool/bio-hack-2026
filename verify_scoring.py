from api.services.prediction_service import PredictionService
from api.schemas.prediction import PredictionRequest

service = PredictionService()

def test_prediction(name, data, expected_range):
    print(f"Testing {name}...")
    try:
        req = PredictionRequest(**data)
        response = service.predict(req)
        score = response.viability_score
        classification = response.classification
        print(f"Result: Score={score}, Class={classification}")
        
        if expected_range[0] <= score <= expected_range[1]:
            print("✅ PASS")
        else:
            print(f"❌ FAIL: Expected {expected_range}, got {score}")
            
        print(f"Risk Factors: {response.risk_factors}")
        print("-" * 20)
    except Exception as e:
        print(f"❌ ERROR: {e}")

# Test Case 1: Perfect Organ
# Stiffness ~ 15 (Norm ~ 0.7), RI ~ 0.6 (Norm ~ 0.66), Uniformity 95 (0.95), Echo 1 (1.0), Edema 0.2 (1.0), KDPI 10 (0.9), CIT 10 (0.8), Age 30 (0.66), COD (0.5)
perfect_data = {
    "organ_type": "Kidney",
    "tissue_stiffness_kpa": 15.0,
    "resistive_index": 0.6,
    "shear_wave_velocity_ms": 2.0,
    "perfusion_uniformity_pct": 98.0,
    "echogenicity_grade": 1,
    "edema_index": 0.25,
    "cold_ischemia_hours": 8.0,
    "donor_age": 25,
    "kdpi_percentile": 10,
    "cause_of_death": "Trauma",
    "warm_ischemia_minutes": 20.0
}

# Test Case 2: Marginal Organ
# Stiffness ~ 25 (Norm ~ 0.5), RI ~ 0.75 (Norm ~ 0.4), Uniformity 80 (0.8), Echo 2 (0.75), Edema 0.35 (0.6), KDPI 60 (0.4), CIT 20 (0.6), Age 55 (0.4), COD (0.5)
marginal_data = {
    "organ_type": "Kidney",
    "tissue_stiffness_kpa": 25.0,
    "resistive_index": 0.75,
    "shear_wave_velocity_ms": 3.0,
    "perfusion_uniformity_pct": 80.0,
    "echogenicity_grade": 2,
    "edema_index": 0.35,
    "cold_ischemia_hours": 20.0,
    "donor_age": 55,
    "kdpi_percentile": 60,
    "cause_of_death": "CVA",
    "warm_ischemia_minutes": 30.0
}

# Test Case 3: Decline Organ
# Stiffness ~ 40 (Norm ~ 0.2), RI ~ 0.9 (Norm ~ 0.16), Uniformity 50 (0.5), Echo 4 (0.25), Edema 0.5 (0.25), KDPI 90 (0.1), CIT 30 (0.4), Age 75 (0.16), COD (0.5)
decline_data = {
    "organ_type": "Kidney",
    "tissue_stiffness_kpa": 40.0,
    "resistive_index": 0.9,
    "shear_wave_velocity_ms": 4.0,
    "perfusion_uniformity_pct": 50.0,
    "echogenicity_grade": 4,
    "edema_index": 0.5,
    "cold_ischemia_hours": 30.0,
    "donor_age": 75,
    "kdpi_percentile": 90,
    "cause_of_death": "CVA",
    "warm_ischemia_minutes": 60.0
}

test_prediction("Perfect Organ", perfect_data, (80, 100))
test_prediction("Marginal Organ", marginal_data, (40, 79))
test_prediction("Decline Organ", decline_data, (0, 39))
