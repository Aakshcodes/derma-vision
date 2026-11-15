import json
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ai_engine.inference.pipeline import DermaVisionPipeline
from ..models.entities import Analysis, User
from .storage_service import StorageService


class AnalysisService:
    def __init__(self):
        # Initialize singleton AI pipeline
        self.pipeline = DermaVisionPipeline()
        self.storage = StorageService()

    def analyze_and_store(
        self,
        db: Session,
        user_id: str,
        image_bytes: bytes,
        anatomical_site: str = "Unspecified",
    ) -> Tuple[bool, Dict]:
        """
        Executes quality gate -> AI inference -> storage -> database persistence.
        """
        # Run AI Pipeline
        result = self.pipeline.analyze(image_bytes, anatomical_site=anatomical_site)

        if result["status"] == "FAILED_QUALITY":
            return False, result

        # Extract results
        pred = result["prediction"]
        guidance = result["clinical_guidance"]
        images = result["images"]

        # Persist images to disk
        analysis_id = str(uuid.uuid4())

        orig_rel, heat_rel, over_rel = self.storage.save_analysis_images(
            analysis_id=analysis_id,
            original_rgb=images["original_rgb"],
            heatmap_rgb=images["heatmap_rgb"],
            overlay_rgb=images["overlay_rgb"],
        )

        # Create database entity
        analysis_record = Analysis(
            id=analysis_id,
            user_id=user_id,
            predicted_category=pred["predicted_category"],
            confidence_score=pred["confidence"],
            is_uncertain=pred["is_uncertain"],
            status="COMPLETED",
            anatomical_site=anatomical_site,
            raw_image_path=orig_rel,
            heatmap_path=heat_rel,
            overlay_path=over_rel,
            calibrated_probabilities=json.dumps(pred["calibrated_probabilities"]),
            clinical_summary=guidance["summary"],
            recommendations=json.dumps(guidance["recommendations"]),
            created_at=datetime.now(timezone.utc),
        )

        db.add(analysis_record)
        db.commit()
        db.refresh(analysis_record)

        response_payload = {
            "id": analysis_record.id,
            "status": "COMPLETED",
            "anatomical_site": anatomical_site,
            "prediction": {
                "category": analysis_record.predicted_category,
                "confidence": analysis_record.confidence_score,
                "calibrated_probabilities": pred["calibrated_probabilities"],
                "uncertainty_score": pred.get("entropy", 0.0),
                "is_inconclusive": analysis_record.is_uncertain,
            },
            "visualizations": {
                "original_image_url": f"/api/v1/media/{orig_rel}",
                "heatmap_url": f"/api/v1/media/{heat_rel}",
                "overlay_url": f"/api/v1/media/{over_rel}",
            },
            "clinical_guidance": {
                "triage_level": guidance["triage_level"],
                "summary": guidance["summary"],
                "recommendations": guidance["recommendations"],
                "dermatologist_consult_advised": guidance["dermatologist_consult_advised"],
            },
            "created_at": analysis_record.created_at,
        }

        return True, response_payload

    def get_user_history(
        self,
        db: Session,
        user_id: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict]:
        records = (
            db.query(Analysis)
            .filter(Analysis.user_id == user_id)
            .order_by(desc(Analysis.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        return [
            {
                "id": r.id,
                "predicted_category": r.predicted_category,
                "confidence_score": r.confidence_score,
                "is_uncertain": r.is_uncertain,
                "anatomical_site": r.anatomical_site,
                "thumbnail_url": f"/api/v1/media/{r.overlay_path or r.raw_image_path}",
                "created_at": r.created_at,
            }
            for r in records
        ]

    def delete_analysis(
        self,
        db: Session,
        user_id: str,
        analysis_id: str,
    ) -> bool:
        record = (
            db.query(Analysis)
            .filter(Analysis.id == analysis_id, Analysis.user_id == user_id)
            .first()
        )
        if not record:
            return False

        # Delete image files
        self.storage.delete_analysis_images(
            raw_path=record.raw_image_path,
            heat_path=record.heatmap_path,
            over_path=record.overlay_path,
        )

        db.delete(record)
        db.commit()
        return True


analysis_service = AnalysisService()
