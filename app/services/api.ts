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
  const response = await getPrediction(requestData);

  // Map response to AnalysisResult type
  return {
    viability_score: response.viability_score,
    classification: response.classification as AnalysisResult["classification"],
    confidence: response.confidence,
    risk_factors: response.risk_factors,
  };
};
