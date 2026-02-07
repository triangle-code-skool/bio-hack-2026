import { AssessmentFormData, AnalysisResult } from "@/types/assessment";

// Change to your ngrok/Railway URL for real device testing
const BASE_URL = "http://localhost:8000";

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
  feature_contributions?: Record<string, number>;
}

/**
 * Transform camelCase form data to snake_case API request format
 */
export const transformFormDataToRequest = (
  formData: AssessmentFormData,
): PredictionRequest => {
  const { ultrasound, clinical } = formData;

  return {
    organ_type: clinical.organType ?? "Kidney",
    tissue_stiffness_kpa: ultrasound.tissueStiffness ?? 0,
    resistive_index: ultrasound.resistiveIndex ?? 0,
    shear_wave_velocity_ms: ultrasound.shearWaveVelocity ?? 0,
    perfusion_uniformity_pct: ultrasound.perfusionUniformity,
    echogenicity_grade: ultrasound.echogenicityGrade,
    edema_index: ultrasound.edemaIndex,
    cold_ischemia_hours: clinical.coldIschemiaTime ?? 0,
    donor_age: clinical.donorAge ?? 0,
    kdpi_percentile: clinical.kdpiDriScore ?? undefined,
    cause_of_death: clinical.causeOfDeath ?? "Other",
    warm_ischemia_minutes: clinical.warmIschemiaTime ?? 0,
  };
};

/**
 * Make prediction API call
 */
export const getPrediction = async (
  data: PredictionRequest,
): Promise<PredictionResponse> => {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Prediction failed: ${response.status} - ${errorText}`);
  }

  return await response.json();
};

/**
 * High-level function to predict organ viability from form data
 */
export const predictViability = async (
  formData: AssessmentFormData,
): Promise<AnalysisResult> => {
  const requestData = transformFormDataToRequest(formData);

  try {
    const response = await getPrediction(requestData);

    // Map response to AnalysisResult type
    return {
      viability_score: response.viability_score,
      classification:
        response.classification as AnalysisResult["classification"],
      confidence: response.confidence,
      risk_factors: response.risk_factors,
    };
  } catch (error) {
    console.warn("Backend Offline, using simulation mode", error);

    // --- FALLBACK MOCK LOGIC (Matches Streamlit) ---
    const {
      tissue_stiffness_kpa: stiffness,
      resistive_index: ri,
      cold_ischemia_hours: cit_hours,
      donor_age,
      perfusion_uniformity_pct: perfusion,
    } = requestData;

    let score = 100;
    score -= stiffness > 6.0 ? (stiffness - 5.0) * 3 : 0;
    score -= ri > 0.7 ? (ri - 0.7) * 40 : 0;
    score -= cit_hours > 12 ? (cit_hours - 12) * 1.5 : 0;
    score -= donor_age > 50 ? (donor_age - 50) * 0.3 : 0;
    score -= (100 - perfusion) * 0.2;

    score = Math.max(0, Math.min(100, score));

    let classification: AnalysisResult["classification"] = "Decline";
    let msg = "";

    if (score >= 70) {
      classification = "Accept";
      msg = "Organ shows excellent viability parameters. (SIMULATED)";
    } else if (score >= 40) {
      classification = "Marginal";
      msg = "Organ shows signs of stress. (SIMULATED)";
    } else {
      classification = "Decline";
      msg = "High risk features detected. (SIMULATED)";
    }

    return {
      viability_score: Math.round(score),
      classification,
      confidence: 0.87,
      risk_factors: [msg],
    };
  }
};
