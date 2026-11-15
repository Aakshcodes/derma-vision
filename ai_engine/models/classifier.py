"""
DermaVision AI — Neural Classifier & Uncertainty Calibration Engine
MobileNetV3-Large with Calibrated Softmax and Entropy-based Out-of-Distribution Handling.
"""

from typing import Dict, List, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import models


CLASS_NAMES = ["Acne", "Eczema", "Normal"]
CLASS_DESCRIPTIONS = {
    "Acne": "Inflammatory or comedonal acneiform lesions (e.g. papules, pustules).",
    "Eczema": "Erythematous, scaly, or pruritic patches indicative of atopic/contact dermatitis.",
    "Normal": "Healthy baseline epidermal tissue without active focal lesions.",
}


class DermaVisionClassifier(nn.Module):
    """
    MobileNetV3-Large tailored for lightweight, low-latency skin condition screening.
    Supports temperature scaling for calibrated posterior probability estimation.
    """

    def __init__(
        self,
        num_classes: int = len(CLASS_NAMES),
        temperature: float = 1.35,
        uncertainty_threshold: float = 0.58,
        entropy_threshold: float = 0.95,
        pretrained: bool = False,
    ):
        super().__init__()
        self.num_classes = num_classes
        self.temperature = nn.Parameter(torch.tensor([temperature]), requires_grad=False)
        self.uncertainty_threshold = uncertainty_threshold
        self.entropy_threshold = entropy_threshold

        # Load MobileNetV3-Large architecture
        weights = models.MobileNet_V3_Large_Weights.DEFAULT if pretrained else None
        base_model = models.mobilenet_v3_large(weights=weights)

        # Retain feature extractor (all inverted residual bottlenecks)
        self.features = base_model.features
        self.avgpool = base_model.avgpool

        # Replace classification head with custom bottleneck
        in_features = 960  # MobileNetV3-Large final pooling channels
        self.classifier = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.Hardswish(),
            nn.Dropout(p=0.25),
            nn.Linear(256, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Raw forward pass returning unscaled logits."""
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        logits = self.classifier(x)
        return logits

    def get_target_gradcam_layer(self) -> nn.Module:
        """Returns the final convolutional block for Grad-CAM hooking."""
        return self.features[-1]

    def predict_calibrated(
        self,
        x: torch.Tensor,
    ) -> Dict:
        """
        Executes calibrated inference:
        1. Forward pass for logits
        2. Softmax with Temperature Scaling
        3. Shannon Entropy computation
        4. Uncertainty flag check
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            calibrated_logits = logits / self.temperature
            probs = F.softmax(calibrated_logits, dim=-1)[0]

            # Shannon entropy: H(P) = -sum(p * log(p))
            entropy = -float(torch.sum(probs * torch.log(probs + 1e-12)).item())
            top_prob, top_idx = torch.max(probs, dim=-1)

            top_prob_val = float(top_prob.item())
            top_class = CLASS_NAMES[top_idx.item()]

            # Uncertainty rule
            is_uncertain = (
                top_prob_val < self.uncertainty_threshold
                or entropy > self.entropy_threshold
            )

            probabilities_dict = {
                CLASS_NAMES[i]: round(float(probs[i].item()), 4)
                for i in range(self.num_classes)
            }

            return {
                "predicted_category": "Inconclusive" if is_uncertain else top_class,
                "confidence": round(top_prob_val, 4),
                "is_uncertain": is_uncertain,
                "entropy": round(entropy, 4),
                "calibrated_probabilities": probabilities_dict,
                "description": CLASS_DESCRIPTIONS.get(top_class, ""),
            }
