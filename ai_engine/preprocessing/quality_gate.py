"""
DermaVision AI — Image Quality Gatekeeper Engine
Validates raw photographic inputs before neural network inference to prevent unreliable predictions.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image


@dataclass
class QualityMetric:
    name: str
    value: float
    threshold: float
    passed: bool
    advice: str


@dataclass
class QualityResult:
    is_valid: bool
    error_code: Optional[str] = None
    message: Optional[str] = None
    metrics: List[QualityMetric] = field(default_factory=list)
    normalized_image: Optional[np.ndarray] = None


class ImageQualityGatekeeper:
    """
    Enforces clinical imaging standards prior to deep learning classification:
    1. Resolution & Dimension check
    2. Motion blur & focus check (Laplacian variance)
    3. Exposure & Lighting check (Luminance histogram)
    4. Skin area verification (HSV / YCbCr color distribution)
    """

    def __init__(
        self,
        min_width: int = 256,
        min_height: int = 256,
        blur_threshold: float = 75.0,
        min_luminance: float = 38.0,
        max_luminance: float = 228.0,
        min_skin_ratio: float = 0.12,
    ):
        self.min_width = min_width
        self.min_height = min_height
        self.blur_threshold = blur_threshold
        self.min_luminance = min_luminance
        self.max_luminance = max_luminance
        self.min_skin_ratio = min_skin_ratio

    def validate_image_array(self, image_bgr: np.ndarray) -> QualityResult:
        if image_bgr is None or image_bgr.size == 0:
            return QualityResult(
                is_valid=False,
                error_code="INVALID_IMAGE_DATA",
                message="The uploaded file could not be parsed as a valid image.",
            )

        h, w = image_bgr.shape[:2]
        metrics: List[QualityMetric] = []

        # 1. Dimension Check
        dimension_passed = w >= self.min_width and h >= self.min_height
        metrics.append(
            QualityMetric(
                name="resolution",
                value=float(min(w, h)),
                threshold=float(min(self.min_width, self.min_height)),
                passed=dimension_passed,
                advice="Image resolution is too low. Please upload a higher resolution capture.",
            )
        )
        if not dimension_passed:
            return QualityResult(
                is_valid=False,
                error_code="RESOLUTION_TOO_LOW",
                message=f"Image dimension ({w}x{h}) is below the required {self.min_width}x{self.min_height}.",
                metrics=metrics,
            )

        # 2. Luminance / Exposure Check
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        mean_luminance = float(np.mean(gray))
        lum_passed = self.min_luminance <= mean_luminance <= self.max_luminance
        advice_lum = (
            "Lighting is too dark. Turn on camera flash or move to a well-lit area."
            if mean_luminance < self.min_luminance
            else "Lighting is overexposed or washed out. Reduce glare and direct reflections."
        )
        metrics.append(
            QualityMetric(
                name="luminance",
                value=round(mean_luminance, 2),
                threshold=self.min_luminance,
                passed=lum_passed,
                advice=advice_lum,
            )
        )
        if not lum_passed:
            code = "UNDEREXPOSED" if mean_luminance < self.min_luminance else "OVEREXPOSED"
            return QualityResult(
                is_valid=False,
                error_code=f"POOR_LIGHTING_{code}",
                message=advice_lum,
                metrics=metrics,
            )

        # 3. Blur / Sharpness Check (Laplacian Variance)
        laplacian_var = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        blur_passed = laplacian_var >= self.blur_threshold
        metrics.append(
            QualityMetric(
                name="sharpness",
                value=round(laplacian_var, 2),
                threshold=self.blur_threshold,
                passed=blur_passed,
                advice="Camera motion or focus blur detected. Hold your device steady and retake.",
            )
        )
        if not blur_passed:
            return QualityResult(
                is_valid=False,
                error_code="IMAGE_TOO_BLURRY",
                message="Photograph is too blurry for reliable dermatological assessment.",
                metrics=metrics,
            )

        # 4. Human Skin Tone Area Check (HSV & YCrCb mask)
        hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        ycrcb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2YCrCb)

        # HSV skin range (broad to support diverse skin tones from Fitzpatrick I to VI)
        lower_hsv = np.array([0, 20, 50], dtype=np.uint8)
        upper_hsv = np.array([30, 255, 255], dtype=np.uint8)
        mask_hsv = cv2.inRange(hsv, lower_hsv, upper_hsv)

        # YCrCb skin range
        lower_ycrcb = np.array([0, 133, 77], dtype=np.uint8)
        upper_ycrcb = np.array([255, 173, 127], dtype=np.uint8)
        mask_ycrcb = cv2.inRange(ycrcb, lower_ycrcb, upper_ycrcb)

        skin_mask = cv2.bitwise_or(mask_hsv, mask_ycrcb)
        skin_ratio = float(np.count_nonzero(skin_mask) / (h * w))

        skin_passed = skin_ratio >= self.min_skin_ratio
        metrics.append(
            QualityMetric(
                name="skin_presence",
                value=round(skin_ratio, 3),
                threshold=self.min_skin_ratio,
                passed=skin_passed,
                advice="Clothing, fabric, or non-skin surface detected. Please remove clothing from the focus area and point camera directly at exposed skin.",
            )
        )
        if not skin_passed:
            return QualityResult(
                is_valid=False,
                error_code="NO_SKIN_SURFACE_DETECTED",
                message="Clothing or non-skin surface detected. Please frame bare human skin directly in the reticle.",
                metrics=metrics,
            )

        return QualityResult(
            is_valid=True,
            metrics=metrics,
            normalized_image=image_bgr,
        )

    def validate_file_bytes(self, file_bytes: bytes) -> QualityResult:
        np_arr = np.frombuffer(file_bytes, np.uint8)
        image_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return self.validate_image_array(image_bgr)
