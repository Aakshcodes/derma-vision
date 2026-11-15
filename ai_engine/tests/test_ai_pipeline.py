"""
Automated Test Suite for DermaVision AI Engine
Tests Image Quality Gatekeeper, MobileNetV3 Classifier, and Grad-CAM Generation.
"""

import cv2
import numpy as np
import pytest
import torch

from ai_engine.explainability.gradcam import GradCAM
from ai_engine.inference.pipeline import DermaVisionPipeline
from ai_engine.models.classifier import CLASS_NAMES, DermaVisionClassifier
from ai_engine.preprocessing.quality_gate import ImageQualityGatekeeper


def create_synthetic_skin_image(
    width: int = 300,
    height: int = 300,
    blur: bool = False,
    is_skin: bool = True,
    luminance: int = 150,
) -> np.ndarray:
    """Helper to generate controlled synthetic images for validation."""
    if not is_skin:
        # Uniform gray image (non-skin)
        img = np.full((height, width, 3), luminance, dtype=np.uint8)
    else:
        # Base skin tone in BGR (approx RGB [220, 160, 140] -> BGR [140, 160, 220])
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :] = [140, 160, 220]

        # Add simulated lesion texture / papule in the center
        cv2.circle(img, (width // 2, height // 2), 25, (40, 50, 180), -1)
        # Add high-frequency noise / pores
        noise = np.random.normal(0, 10, (height, width, 3)).astype(np.int16)
        img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    if blur:
        img = cv2.GaussianBlur(img, (25, 25), 0)

    return img


def test_quality_gate_rejects_low_resolution():
    gate = ImageQualityGatekeeper(min_width=256, min_height=256)
    tiny_img = create_synthetic_skin_image(width=100, height=100)
    result = gate.validate_image_array(tiny_img)

    assert not result.is_valid
    assert result.error_code == "RESOLUTION_TOO_LOW"


def test_quality_gate_rejects_blurry_image():
    gate = ImageQualityGatekeeper(blur_threshold=60.0)
    blurry_img = create_synthetic_skin_image(width=300, height=300, blur=True)
    result = gate.validate_image_array(blurry_img)

    assert not result.is_valid
    assert result.error_code == "IMAGE_TOO_BLURRY"


def test_quality_gate_rejects_non_skin_or_dark():
    gate = ImageQualityGatekeeper()
    black_img = np.zeros((300, 300, 3), dtype=np.uint8)
    result = gate.validate_image_array(black_img)

    assert not result.is_valid
    assert "LIGHTING" in result.error_code or "NO_SKIN" in result.error_code


def test_quality_gate_accepts_valid_skin_image():
    gate = ImageQualityGatekeeper(blur_threshold=40.0)
    valid_skin = create_synthetic_skin_image(width=300, height=300, blur=False)
    result = gate.validate_image_array(valid_skin)

    assert result.is_valid
    assert result.normalized_image is not None


def test_classifier_forward_pass_and_calibration():
    model = DermaVisionClassifier(num_classes=3)
    dummy_input = torch.randn(1, 3, 224, 224)

    # Test raw forward logits
    logits = model(dummy_input)
    assert logits.shape == (1, 3)

    # Test calibrated prediction
    pred = model.predict_calibrated(dummy_input)
    assert "predicted_category" in pred
    assert "confidence" in pred
    assert "calibrated_probabilities" in pred

    probs = pred["calibrated_probabilities"]
    assert len(probs) == 3
    prob_sum = sum(probs.values())
    assert pytest.approx(prob_sum, rel=1e-2) == 1.0


def test_gradcam_generation():
    model = DermaVisionClassifier(num_classes=3)
    target_layer = model.get_target_gradcam_layer()
    gradcam = GradCAM(model, target_layer)

    dummy_input = torch.randn(1, 3, 224, 224)
    heatmap = gradcam.generate(dummy_input, target_class_idx=0)

    assert isinstance(heatmap, np.ndarray)
    assert heatmap.ndim == 2
    assert 0.0 <= np.max(heatmap) <= 1.0
    assert np.min(heatmap) >= 0.0

    # Test overlay blending
    dummy_rgb = np.full((224, 224, 3), 180, dtype=np.uint8)
    colored_hm, overlay = GradCAM.overlay_heatmap(heatmap, dummy_rgb)
    assert overlay.shape == dummy_rgb.shape
    assert colored_hm.shape == dummy_rgb.shape


def test_pipeline_end_to_end_success():
    pipeline = DermaVisionPipeline()
    valid_skin_bgr = create_synthetic_skin_image(width=300, height=300)

    # Encode to JPEG bytes
    success, buffer = cv2.imencode(".jpg", valid_skin_bgr)
    assert success
    jpg_bytes = buffer.tobytes()

    result = pipeline.analyze(jpg_bytes, anatomical_site="Forearm")

    assert result["status"] == "COMPLETED"
    assert result["anatomical_site"] == "Forearm"
    assert "prediction" in result
    assert "clinical_guidance" in result
    assert "images" in result
    assert result["images"]["overlay_rgb"] is not None
