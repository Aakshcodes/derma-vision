"""
DermaVision AI — Unified AI Inference & Analysis Pipeline
Orchestrates Image Quality Validation -> Tensor Preprocessing -> Calibrated Classification -> Grad-CAM Generation -> Clinical Guidance.
"""

import io
from typing import Dict, Optional, Tuple
import cv2
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

try:
    from ai_engine.explainability.gradcam import GradCAM
    from ai_engine.models.classifier import CLASS_NAMES, DermaVisionClassifier
    from ai_engine.preprocessing.quality_gate import ImageQualityGatekeeper, QualityResult
except ImportError:
    from ..explainability.gradcam import GradCAM
    from ..models.classifier import CLASS_NAMES, DermaVisionClassifier
    from ..preprocessing.quality_gate import ImageQualityGatekeeper, QualityResult


class DermaVisionPipeline:
    """
    End-to-end inference service for DermaVision AI.
    """

    def __init__(
        self,
        weights_path: Optional[str] = None,
        device: Optional[str] = None,
    ):
        self.device = torch.device(
            device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        )

        # 1. Quality gatekeeper
        self.quality_gate = ImageQualityGatekeeper()

        # 2. Classifier
        self.model = DermaVisionClassifier().to(self.device)
        if weights_path:
            state_dict = torch.load(weights_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
        self.model.eval()

        # 3. Grad-CAM hooked to final convolutional layer
        target_layer = self.model.get_target_gradcam_layer()
        self.gradcam = GradCAM(self.model, target_layer)

        # 4. Standard preprocessing pipeline for MobileNetV3
        self.transform = transforms.Compose(
            [
                transforms.Resize((256, 256)),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

    def analyze(
        self,
        image_bytes: bytes,
        anatomical_site: str = "Unspecified",
    ) -> Dict:
        """
        Executes end-to-end validation, inference, and explainability.
        """
        # Step 1: Pre-inference Image Quality Gate
        quality: QualityResult = self.quality_gate.validate_file_bytes(image_bytes)
        if not quality.is_valid:
            return {
                "status": "FAILED_QUALITY",
                "error_code": quality.error_code,
                "message": quality.message,
                "metrics": [
                    {
                        "name": m.name,
                        "value": m.value,
                        "threshold": m.threshold,
                        "passed": m.passed,
                        "advice": m.advice,
                    }
                    for m in quality.metrics
                ],
            }

        # Step 2: Image Decoding & Preprocessing
        image_bgr = quality.normalized_image
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(image_rgb)

        input_tensor = self.transform(pil_img).unsqueeze(0).to(self.device)

        # Step 3: Calibrated Prediction & Uncertainty Handling
        prediction = self.model.predict_calibrated(input_tensor)

        # Step 4: Grad-CAM Explainability Generation
        pred_category = prediction["predicted_category"]
        class_idx = (
            CLASS_NAMES.index(pred_category)
            if pred_category in CLASS_NAMES
            else 0
        )

        heatmap = self.gradcam.generate(input_tensor, target_class_idx=class_idx)
        colored_heatmap_rgb, blended_overlay_rgb = GradCAM.overlay_heatmap(
            heatmap=heatmap,
            original_rgb=image_rgb,
            alpha=0.55,
        )

        # Step 5: Clinical Guidance & Triage Formulation
        guidance = self._formulate_clinical_guidance(
            category=pred_category,
            confidence=prediction["confidence"],
            is_uncertain=prediction["is_uncertain"],
        )

        return {
            "status": "COMPLETED",
            "prediction": prediction,
            "anatomical_site": anatomical_site,
            "clinical_guidance": guidance,
            "images": {
                "original_rgb": image_rgb,
                "heatmap_rgb": colored_heatmap_rgb,
                "overlay_rgb": blended_overlay_rgb,
            },
        }

    def _formulate_clinical_guidance(
        self,
        category: str,
        confidence: float,
        is_uncertain: bool,
    ) -> Dict:
        if is_uncertain:
            return {
                "triage_level": "INCONCLUSIVE",
                "summary": "Visual features were ambiguous or outside calibrated confidence bounds.",
                "recommendations": [
                    "Ensure photos are taken under bright, indirect natural sunlight.",
                    "Have this skin region visually inspected by a certified dermatologist or general physician.",
                ],
                "dermatologist_consult_advised": True,
            }

        if category == "Acne":
            return {
                "triage_level": "MILD_SELF_CARE",
                "summary": "Visual pattern resembles inflammatory acneiform comedones or papules.",
                "recommendations": [
                    "Cleanse twice daily with a gentle, non-comedogenic foaming cleanser.",
                    "Avoid manual picking or popping to prevent post-inflammatory hyperpigmentation and scarring.",
                    "If deep cystic nodules or painful inflammation develops, consult a dermatologist.",
                ],
                "dermatologist_consult_advised": False,
            }
        elif category == "Eczema":
            return {
                "triage_level": "MODERATE_EVALUATION",
                "summary": "Visual pattern resembles xerotic or eczematous dermatitis with surface flaking.",
                "recommendations": [
                    "Apply fragrance-free ceramide-rich barrier creams immediately after washing.",
                    "Avoid hot showers and known contact irritants or harsh detergents.",
                    "Seek clinical consultation if the area becomes intensely pruritic, warm, or weeps fluid.",
                ],
                "dermatologist_consult_advised": True,
            }
        else:  # Normal
            return {
                "triage_level": "HEALTHY_BASELINE",
                "summary": "Visual pattern aligns with healthy epidermal baseline without active focal lesions.",
                "recommendations": [
                    "Maintain daily broad-spectrum SPF 30+ sun protection.",
                    "Perform monthly self-examinations to monitor changes in existing moles.",
                ],
                "dermatologist_consult_advised": False,
            }
