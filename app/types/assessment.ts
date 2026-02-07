/**
 * UltraViab Assessment Form Types
 */

export type OrganType = "Kidney" | "Liver" | "Heart" | "Lung";

export type CauseOfDeath = "Trauma" | "CVA" | "Anoxia" | "Other";

export type EchogenicityGrade = 1 | 2 | 3 | 4 | 5;

export interface UltrasoundMetrics {
  tissueStiffness: number | null; // kPa
  resistiveIndex: number | null; // decimal (0-1)
  shearWaveVelocity: number | null; // m/s
  perfusionUniformity: number; // 0-100%
  echogenicityGrade: EchogenicityGrade; // 1-5
  edemaIndex: number; // 0-10
}

export interface ClinicalMetadata {
  organType: OrganType | null;
  coldIschemiaTime: number | null; // hours
  warmIschemiaTime: number | null; // minutes
  donorAge: number | null; // years
  kdpiDriScore: number | null; // percentile
  causeOfDeath: CauseOfDeath | null;
}

export interface AssessmentFormData {
  ultrasound: UltrasoundMetrics;
  clinical: ClinicalMetadata;
}

export const initialFormData: AssessmentFormData = {
  ultrasound: {
    tissueStiffness: null,
    resistiveIndex: null,
    shearWaveVelocity: null,
    perfusionUniformity: 50,
    echogenicityGrade: 3,
    edemaIndex: 5,
  },
  clinical: {
    organType: null,
    coldIschemiaTime: null,
    warmIschemiaTime: null,
    donorAge: null,
    kdpiDriScore: null,
    causeOfDeath: null,
  },
};

/**
 * API Response Types
 */

export type Classification = "Accept" | "Marginal" | "Decline";

export interface AnalysisResult {
  viability_score: number; // 0-100
  classification: Classification;
  confidence: number; // 0-1
  risk_factors: string[];
}

/**
 * Mock API Response
 */
export const mockAnalysisResult: AnalysisResult = {
  viability_score: 78,
  classification: "Accept",
  confidence: 0.89,
  risk_factors: ["cold_ischemia_hours approaching threshold"],
};
