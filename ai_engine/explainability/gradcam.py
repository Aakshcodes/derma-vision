"""
DermaVision AI — Explainable AI (Grad-CAM) Module
Extracts gradient-weighted class activation maps from the final convolutional layer
to provide transparent visual feedback on where the neural network focused.
"""

from typing import Optional, Tuple
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class GradCAM:
    """
    Implements Grad-CAM (Gradient-Weighted Class Activation Mapping) for PyTorch models.
    Hooks into the final convolutional feature extractor layer.
    """

    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients: Optional[torch.Tensor] = None
        self.activations: Optional[torch.Tensor] = None

        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0].detach()

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate(
        self,
        input_tensor: torch.Tensor,
        target_class_idx: Optional[int] = None,
    ) -> np.ndarray:
        """
        Generates a 2D normalized Grad-CAM heatmap for the given input tensor.
        input_tensor: Shape (1, C, H, W)
        target_class_idx: If None, uses the highest scoring class.
        Returns: 2D numpy array [0.0, 1.0] of shape (H, W).
        """
        self.model.eval()
        self.model.zero_grad()

        # Forward pass
        logits = self.model(input_tensor)

        if target_class_idx is None:
            target_class_idx = int(torch.argmax(logits, dim=1).item())

        # Target class score
        score = logits[0, target_class_idx]
        score.backward(retain_graph=True)

        if self.gradients is None or self.activations is None:
            raise RuntimeError("Grad-CAM hooks failed to capture gradients or activations.")

        # Global average pooling of gradients: alpha_k = (1/Z) * sum(grad)
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])  # Shape (Channels,)

        # Weight the channels by corresponding gradients
        activations = self.activations[0]  # Shape (Channels, H_feat, W_feat)
        for i in range(activations.size(0)):
            activations[i, :, :] *= pooled_gradients[i]

        # Heatmap is the ReLU of weighted channel sum
        heatmap = torch.sum(activations, dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0.0)  # ReLU

        # Normalize to [0, 1]
        max_val = np.max(heatmap)
        if max_val > 1e-8:
            heatmap = heatmap / max_val
        else:
            heatmap = np.zeros_like(heatmap)

        return heatmap

    @staticmethod
    def overlay_heatmap(
        heatmap: np.ndarray,
        original_rgb: np.ndarray,
        alpha: float = 0.55,
        colormap: int = cv2.COLORMAP_JET,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resizes heatmap to match original RGB image, applies colormap, and blends.
        Returns:
            heatmap_colored: RGB colormapped heatmap
            overlay: Blended RGB image with heatmap
        """
        h, w = original_rgb.shape[:2]

        # Resize heatmap to input image dimensions
        resized_heatmap = cv2.resize(heatmap, (w, h))

        # Convert to 0-255 uint8
        heatmap_uint8 = np.uint8(255 * resized_heatmap)

        # Apply OpenCV colormap (returns BGR)
        colored_bgr = cv2.applyColorMap(heatmap_uint8, colormap)
        colored_rgb = cv2.cvtColor(colored_bgr, cv2.COLOR_BGR2RGB)

        # Blend
        overlay = np.clip(
            alpha * original_rgb.astype(np.float32) + (1.0 - alpha) * colored_rgb.astype(np.float32),
            0,
            255,
        ).astype(np.uint8)

        return colored_rgb, overlay
