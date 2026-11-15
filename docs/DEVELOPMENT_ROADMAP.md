# DermaVision AI — Development Roadmap, Challenges & Risk Matrix

---

## 1. Phased Development Roadmap

### Phase 0: Discovery, Architecture & Planning (Current Phase)
- Thorough analysis of the reference design image and UI translation to mobile.
- Authoring of core specifications: `PRD.md`, `TRD.md`, `SYSTEM_ARCHITECTURE.md`, `DATABASE_DESIGN.md`, `API_DOCUMENTATION.md`, `AI_MODEL_DOCUMENTATION.md`, `UI_UX_GUIDE.md`.
- Definition of tech stack, boundaries, and acceptance criteria.
- *Deliverable:* Complete project architectural documentation suite.

### Phase 1: Mobile UI/UX & Design System Implementation
- Initialize React Native / Expo TypeScript project with NativeWind and design tokens.
- Implement the "Warm Cream & Charcoal" atomic components: Pill buttons, circular progress rings, dotted list items, and cards.
- Construct the 12 required mobile screens with mock data and complete navigation transitions.
- *Deliverable:* Standalone, interactive mobile UI prototype runnable in Expo Go / Android emulator.

### Phase 2: Backend Foundation & API Services
- Initialize FastAPI project with async SQLAlchemy, Pydantic v2 schemas, and Alembic migrations.
- Set up PostgreSQL schema with `users`, `analyses`, `analysis_visualizations`, and cascade deletion.
- Implement JWT authentication, guest session creation, and secure user management.
- Build image upload endpoint with multipart streaming and SHA256 storage hashing.
- *Deliverable:* Verified backend test suite with working auth, database persistence, and API documentation.

### Phase 3: AI Engine & Grad-CAM Pipeline
- Implement OpenCV-based Image Quality Gatekeeper (Blur Laplacian variance, exposure histogram, HSV skin tone check).
- Build the PyTorch classification model (MobileNetV3-Large with customized 3-class classifier head for Acne, Eczema, Normal skin).
- Implement post-processing Temperature Scaling calibration and uncertainty thresholds.
- Implement custom Grad-CAM module with forward/backward hooks, jet colormap mapping, and image blending.
- *Deliverable:* Standalone Python AI inference test suite verifying accuracy, quality rejection, and Grad-CAM generation.

### Phase 4: Backend & AI Engine Integration
- Wire the PyTorch model and Grad-CAM generator into FastAPI asynchronous worker tasks.
- Implement private storage management with authenticated image serving.
- Persist inference results, calibrated confidence, and visualization paths to PostgreSQL.
- *Deliverable:* End-to-end `POST /api/v1/analysis/process` returning real AI predictions and heatmap overlays.

### Phase 5: Mobile & Backend Integration
- Connect React Native TanStack Query hooks to the FastAPI backend.
- Wire native camera capture and gallery picker to the image analysis flow.
- Render live Grad-CAM side-by-side comparison slider and calibrated confidence dials.
- Implement analysis history list, detail view, and single/all deletion workflows.
- *Deliverable:* Fully functional mobile application communicating with live backend.

### Phase 6: Testing, Edge Cases & Optimization
- Test low-light, blurry, and non-skin photographs to ensure quality gate rejects properly.
- Verify camera permissions, orientation changes, and offline network state handling.
- Audit data privacy and execute account deletion cascade tests.
- *Deliverable:* Production-ready release candidate with automated integration tests.

### Phase 7: Deployment Configuration
- Configure Docker Compose for backend, PostgreSQL, and Nginx reverse proxy.
- Prepare production environment configuration (`.env.production`).
- Generate Android APK / development build guide.
- Complete `README.md` with step-by-step setup instructions.

---

## 2. Technical Challenges & Recommended Solutions

| Technical Challenge | Root Cause | Recommended Engineering Solution |
| :--- | :--- | :--- |
| **Grad-CAM Latency on Mobile** | Generating heatmaps on server and sending high-res images can slow response time. | Downscale feature map generation to $224 \times 224$ and compress the resulting blended JPEG to $\sim 150\text{ KB}$ before transmission. Return response within $< 1.8\text{ seconds}$. |
| **Camera Blur in Real-World Photos** | Smartphone users often hold phones close with camera shake or low light. | Implement a client-side or server-side OpenCV Laplacian variance check ($Var < 85$) that rejects blurry images immediately with clear actionable advice. |
| **Model Overconfidence** | Standard Softmax pushes probabilities to $> 99\%$ even on ambiguous lesions. | Apply Temperature Scaling ($T \approx 1.4$) fitted on validation data, plus an explicit entropy threshold to label ambiguous cases as `UNCERTAIN`. |
| **Diverse Skin Tone Bias** | Computer vision models trained on Eurocentric datasets struggle on darker skin tones. | Benchmark across the Fitzpatrick Phototype scale (Types I–VI) using datasets like Fitzpatrick 17k. Flag under-represented patterns rather than hallucinating predictions. |
| **Medical Privacy & Bodily Photos** | Skin photographs are sensitive biometric/health data. | Never expose public image links. Enforce authenticated streaming, private storage directories, and immediate cascade deletion upon user request. |

---

## 3. Estimated Development Complexity
- **Mobile Frontend (React Native / Expo):** Moderate-High (12 custom screens, camera hardware hooks, interactive comparison slider, warm cream design system).
- **Backend (FastAPI + PostgreSQL):** Moderate (Standard clean architecture, async sessions, auth, cascade deletion).
- **AI/ML & Grad-CAM:** High (Quality gatekeeper, PyTorch hooks, calibrated temperature scaling, image blending).
- **Total Project Horizon:** Modular, structured build across 7 progressive phases.
