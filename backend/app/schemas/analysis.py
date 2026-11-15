from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel


class QualityMetricOut(BaseModel):
    name: str
    value: float
    threshold: float
    passed: bool
    advice: str


class QualityFailureResponse(BaseModel):
    error_code: str
    message: str
    metrics: List[QualityMetricOut]


class PredictionDetails(BaseModel):
    category: str
    confidence: float
    calibrated_probabilities: Dict[str, float]
    uncertainty_score: float
    is_inconclusive: bool


class VisualizationsOut(BaseModel):
    original_image_url: str
    heatmap_url: Optional[str] = None
    overlay_url: Optional[str] = None


class ClinicalGuidanceOut(BaseModel):
    triage_level: str
    summary: str
    recommendations: List[str]
    dermatologist_consult_advised: bool


class AnalysisResponse(BaseModel):
    id: str
    status: str
    anatomical_site: str
    prediction: PredictionDetails
    visualizations: VisualizationsOut
    clinical_guidance: ClinicalGuidanceOut
    created_at: datetime


class AnalysisListItem(BaseModel):
    id: str
    predicted_category: str
    confidence_score: float
    is_uncertain: bool
    anatomical_site: str
    thumbnail_url: str
    created_at: datetime
