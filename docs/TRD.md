# DermaVision AI — Technical Requirements Document (TRD)

**Version:** 1.0.0  
**Stack:** React Native / Expo (Frontend) + FastAPI (Backend) + PyTorch (AI Engine) + PostgreSQL (Database)

---

## 1. System Architecture & Tech Stack Justification

### 1.1 Mobile Client
- **Framework:** **React Native (Expo SDK 51+) with TypeScript**
  - *Justification:* Single cross-platform codebase with native performance, reliable camera abstraction (`expo-camera`), gallery picker (`expo-image-picker`), and standard hardware sensors (accelerometer for camera levelness).
- **Navigation:** **Expo Router (File-based)** or **React Navigation v6**
  - *Justification:* Smooth native transitions, deep linking, modal sheets, and safe-area insets handling.
- **Server State & Caching:** **TanStack React Query v5**
  - *Justification:* Automatic retries, offline cache invalidation, background refetching, and optimistic updates for analysis history.
- **Client State:** **Zustand**
  - *Justification:* Ultra-lightweight (1 KB), no boilerplate, seamless persistence via MMKV or Expo SecureStore for authentication tokens and user preferences.
- **UI Styling:** **NativeWind (Tailwind CSS for React Native) & Custom Design Tokens**
  - *Justification:* Direct parity with web tokens and the uploaded UI design system ("Warm Cream & Charcoal").

### 1.2 Backend API Engine
- **Framework:** **FastAPI (Python 3.11+)**
  - *Justification:* High performance (Starlette/Uvicorn), native asynchronous I/O, automatic OpenAPI 3.1 docs generation, and seamless interoperability with PyTorch tensors without inter-process serialization overhead.
- **Data Validation:** **Pydantic v2**
  - *Justification:* Strict runtime schema enforcement, Rust-backed parsing speed, and type safety across all requests and responses.
- **Security & Auth:** **OAuth2 with Password Bearer (JWT) + bcrypt password hashing**
  - *Justification:* Stateless tokens with refresh rotations, low overhead, and cryptographic signing.

### 1.3 AI/ML Engine
- **Framework:** **PyTorch 2.3+ & Torchvision 0.18+**
  - *Justification:* Industry standard for computer vision research and production deployment. Native hooks (`register_forward_hook`, `register_full_backward_hook`) make Grad-CAM extraction straightforward.
- **Computer Vision Utilities:** **OpenCV (cv2) & Pillow (PIL)**
  - *Justification:* Fast spatial transforms, histogram calculations for blur/exposure quality gates, and color map overlays (`cv2.applyColorMap(..., cv2.COLORMAP_JET)`).
- **Model Format:** **TorchScript / ONNX / Weights State Dict (.pt)**
  - *Justification:* Optimized graph execution for low-latency inference on CPU or CUDA instances.

### 1.4 Database & Persistence
- **Database:** **PostgreSQL 15+**
  - *Justification:* ACID compliance, relational integrity for user scans and audit trails, JSONB column support for flexible model metadata and ABCDE metric tags.
- **ORM & Migrations:** **SQLAlchemy 2.0 (Async) + Alembic**
  - *Justification:* Fully typed async database operations and reproducible schema version control.

### 1.5 Object Storage
- **Storage Strategy:** **Private S3-compatible or local secure filesystem**
  - *Justification:* Medical images must never be publicly readable via unauthenticated URLs. Access is granted exclusively through short-lived presigned URLs ($T_{expiry} \le 15\text{ minutes}$) or authenticated streaming endpoints.

---

## 2. Technical Specifications by Component

### 2.1 Image Validation Engine (Pipeline Stage 1)
```
Input: Raw Image File (multipart/form-data)
Validation Sequence:
  1. Content-Type Check: image/jpeg, image/png, image/webp (Reject SVGs, executables, GIFs)
  2. File Size Bound: 100 KB <= Size <= 15 MB
  3. Resolution Check: Width >= 512px and Height >= 512px
  4. Blur Check (Laplacian Variance):
       var_laplacian = cv2.Laplacian(gray_img, cv2.CV_64F).var()
       If var_laplacian < 85.0 -> Reject with QUALITY_BLURRY
  5. Exposure / Luminance Check:
       mean_luminance = np.mean(gray_img)
       If mean_luminance < 35.0 -> Reject with QUALITY_UNDEREXPOSED
       If mean_luminance > 230.0 -> Reject with QUALITY_OVEREXPOSED
  6. Human Skin Tone Area Check (HSV Space):
       H in [0, 25], S in [0.2, 0.68], V in [0.35, 1.0]
       Skin Pixel Ratio >= 0.15 -> Pass; Else Reject with QUALITY_NO_SKIN_DETECTED
Output: Validated Image Array or Descriptive Validation Error Response
```

### 2.2 Deep Learning Inference & Calibration (Pipeline Stage 2)
- **Input Dimension:** $224 \times 224 \times 3$ or $384 \times 384 \times 3$ (depending on backbone).
- **Normalization:** ImageNet mean $\mu = [0.485, 0.456, 0.406]$ and standard deviation $\sigma = [0.229, 0.224, 0.225]$.
- **Inference Computation:**
  $$\mathbf{z} = f_\theta(\mathbf{x}) \in \mathbb{R}^K \quad (K = 3 \text{ classes})$$
  $$\mathbf{p} = \text{Softmax}\left(\frac{\mathbf{z}}{T}\right), \quad T > 0 \text{ (Learned Temperature)}$$
- **Uncertainty Decision Rule:**
  $$\text{If } \max_k p_k < 0.60 \text{ or } \text{Entropy}(\mathbf{p}) > 0.95 \implies \text{Status: UNCERTAIN}$$

### 2.3 Grad-CAM Explainability Algorithm (Pipeline Stage 3)
1. Forward pass input image through backbone to extract target feature activation map $A^k \in \mathbb{R}^{C \times H \times W}$ from the final convolutional layer (e.g., `features[-1]` in MobileNetV3 or `conv_head` in EfficientNet).
2. Compute gradient of score for predicted class $c$ with respect to feature maps:
   $$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^H \sum_{j=1}^W \frac{\partial y^c}{\partial A_{i,j}^k}$$
3. Compute weighted linear combination and apply ReLU:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left(\sum_k \alpha_k^c A^k\right)$$
4. Upsample $L_{\text{Grad-CAM}}^c$ to original image dimensions, normalize to $[0, 255]$, apply `COLORMAP_JET`, and blend with the original image at $\alpha = 0.55$:
   $$I_{\text{overlay}} = \alpha \cdot I_{\text{original}} + (1 - \alpha) \cdot I_{\text{heatmap}}$$

---

## 3. Directory Layout & Module Structure

```
dermavision-ai/
├── mobile/                  # React Native / Expo Frontend Application
│   ├── app/                 # Expo Router file-based screens
│   ├── components/          # Reusable atomic UI components (Button, Card, Reticle, etc.)
│   ├── hooks/               # Custom React hooks (useCamera, useAnalysis, useAuth)
│   ├── services/            # API client (Axios/Ky instance, Auth endpoints)
│   ├── store/               # Zustand global stores (authStore, scanStore)
│   ├── types/               # TypeScript interface definitions
│   └── constants/           # Design tokens, color palettes, strings
├── backend/                 # FastAPI REST Service
│   ├── app/
│   │   ├── api/v1/          # Versioned route endpoints
│   │   ├── core/            # Configuration, database session, JWT security
│   │   ├── models/          # SQLAlchemy database entities
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── services/        # Business logic (Upload, Storage, Auth)
│   │   └── main.py          # FastAPI application entrypoint
│   ├── tests/               # Pytest automated test suites
│   ├── alembic/             # Database migration scripts
│   └── requirements.txt     # Python dependencies
├── ai-engine/               # Standalone AI/ML Development & Inference Pipeline
│   ├── datasets/            # Dataset acquisition and preprocessing scripts
│   ├── models/              # Model weights (.pt) and architecture classes
│   ├── training/            # PyTorch training, cross-validation, and metrics logging
│   ├── evaluation/          # Confusion matrix, ROC-AUC, calibration curves
│   ├── explainability/      # Custom Grad-CAM and heatmap overlay generators
│   └── inference/           # Production inference wrapper service
├── docs/                    # Complete Architecture and Planning Documents
├── infrastructure/          # Docker compose and deployment manifests
└── README.md
```
