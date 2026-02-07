const BASE_URL = "http://localhost:8000"; // Change to your ngrok/ Railway URL for real device testing

export interface PredictionRequest {
  organ_type: string;
  tissue_stiffness_kpa: number;
  resistive_index: number;
  shear_wave_velocity_ms: number;
  perfusion_uniformity_pct: number;
  echogenicity_grade: number;
  edema_index: number;
  cold_ischemia_hours: number;
  donor_age: number;
  kdpi_percentile?: number;
  cause_of_death: string;
  warm_ischemia_minutes: number;
}

export interface PredictionResponse {
  viability_score: number;
  classification: string;
  confidence: number;
  risk_factors: string[];
  feature_contributions: Record<string, number>;
}

export const getPrediction = async (
  data: PredictionRequest,
): Promise<PredictionResponse> => {
  try {
    const response = await fetch(`${BASE_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error("Prediction request failed");
    }

    return await response.json();
  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};
