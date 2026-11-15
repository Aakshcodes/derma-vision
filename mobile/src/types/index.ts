export interface Prediction {
  category: 'Acne' | 'Eczema' | 'Normal' | 'Inconclusive';
  confidence: number;
  calibrated_probabilities: Record<string, number>;
  uncertainty_score: number;
  is_inconclusive: boolean;
}

export interface Visualizations {
  original_image_url: string;
  heatmap_url?: string;
  overlay_url?: string;
}

export interface ClinicalGuidance {
  triage_level: 'HEALTHY_BASELINE' | 'MILD_SELF_CARE' | 'MODERATE_EVALUATION' | 'INCONCLUSIVE';
  summary: string;
  recommendations: string[];
  dermatologist_consult_advised: boolean;
}

export interface AnalysisRecord {
  id: string;
  status: string;
  anatomical_site: string;
  prediction: Prediction;
  visualizations: Visualizations;
  clinical_guidance: ClinicalGuidance;
  created_at: string;
}

export interface HistoryItem {
  id: string;
  predicted_category: string;
  confidence_score: number;
  is_uncertain: boolean;
  anatomical_site: string;
  thumbnail_url: string;
  created_at: string;
}
