# DermaVision AI — AI/ML Model Architecture, Training & Explainability (Grad-CAM)

**Author:** DermaVision AI Machine Learning Team  
**Framework:** PyTorch 2.3+ / Torchvision  
**Core Scope:** 3-Class Educational Classifier (Acne, Eczema, Normal Skin) + Grad-CAM Visual Heatmaps

---

## 1. Dataset Strategy & Ethical Considerations

### 1.1 Dataset Sources
To ensure robust, diverse, and ethically sound model training, the initial pipeline combines vetted, publicly accessible dermatological and facial benchmark datasets:
1. **DermNet NZ Open Research Dataset:** Extensive photographic captures of acneiform eruptions and eczematous dermatoses across natural lighting conditions.
2. **Fitzpatrick 17k Dataset:** Specifically utilized to audit and balance class performance across the entire Fitzpatrick Skin Phototype scale (Types I through VI) to prevent bias towards lighter skin tones.
3. **ISIC Archive (International Skin Imaging Collaboration):** High-resolution macroscopic and dermoscopic healthy skin baselines.

### 1.2 Data Preprocessing & Augmentation Pipeline
- **Geometric Transformations (Training Only):**
  - Random Horizontal & Vertical Flips ($p = 0.5$)
  - Random Affine Rotation ($-25^\circ \text{ to } +25^\circ$)
  - Color Jitter (Brightness $\pm 0.15$, Contrast $\pm 0.15$, Saturation $\pm 0.1$) to simulate diverse smartphone camera sensors and lighting environments.
- **Inference Preprocessing (Deterministic):**
  - Bilinear Resize to $256 \times 256$ pixels.
  - Center Crop to $224 \times 224$ pixels.
  - Standardization via ImageNet Channel Mean $[0.485, 0.456, 0.406]$ and Std $[0.229, 0.224, 0.225]$.

---

## 2. Model Architecture Comparison & Selection

| Architecture | Parameter Count | ImageNet Top-1 | Inference Latency (CPU) | Storage Footprint | Selection Rationale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MobileNetV3-Large** | **4.2 M** | **75.8%** | **~28 ms** | **~16 MB** | **SELECTED.** Optimal trade-off between high representational capacity, low latency on standard CPU servers, and clean gradient propagation for Grad-CAM. |
| **EfficientNet-B0** | 5.3 M | 77.1% | ~46 ms | ~21 MB | Strong candidate; slightly higher computational complexity during backward hook execution. |
| **ResNet-50** | 25.6 M | 76.1% | ~110 ms | ~98 MB | Unnecessarily heavy for 3-class classification; higher memory overhead without significant accuracy gains. |

---

## 3. Explainability via Grad-CAM (Gradient-Weighted Class Activation Mapping)

### 3.1 Mathematical Foundation
Grad-CAM produces visual explanations for decisions from any CNN-based network without architectural alterations or retraining.

Given an input image and a classification category $c$:
1. We compute the gradient of the unnormalized class score $y^c$ with respect to feature activation maps $A^k$ of a convolutional layer:
   $$\frac{\partial y^c}{\partial A^k}$$
2. We global-average-pool these gradients over width ($W$) and height ($H$) to capture the importance weight $\alpha_k^c$ of feature map $k$:
   $$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^H \sum_{j=1}^W \frac{\partial y^c}{\partial A_{i,j}^k}$$
3. We perform a weighted combination of forward activation maps and pass the result through a Rectified Linear Unit (ReLU) to isolate features that positively contribute to the target class:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$

### 3.2 Target Layer Hooking
In **MobileNetV3-Large**, the hook is attached to the final depthwise-separable block in `model.features[-1]`, capturing rich semantic representations before spatial pooling.

---

## 4. Confidence Calibration & Uncertainty Rejection

### 4.1 Temperature Scaling
Modern neural networks often exhibit overconfident softmax probabilities. We employ **Temperature Scaling**—a single-parameter post-processing calibration that does not alter classification accuracy:
$$\hat{p}_i = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$
Where $T > 0$ is optimized on the validation set via Negative Log-Likelihood minimization.

### 4.2 Rejection Rules (Safety Mechanism)
An inference request is flagged as `UNCERTAIN` or `INCONCLUSIVE` if:
1. $\max_i \hat{p}_i < 0.60$ (Confidence threshold)
2. $\text{Entropy}(\hat{\mathbf{p}}) = -\sum_{i=1}^K \hat{p}_i \log \hat{p}_i > 0.95$ (High dispersion across classes)

When triggered, the user is presented with:
> *"The visual features were indeterminate. DermaVision AI could not confidently identify this pattern. We strongly recommend having this examined by a certified healthcare professional."*
