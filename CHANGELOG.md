# Changelog

All notable changes to the **DermaVision AI** project are documented here.

## [1.0.0] — Initial Production-Quality MVP Release

### Architecture & Documentation
- Established comprehensive documentation suite in `docs/`:
  - `PRD.md`, `TRD.md`, `SYSTEM_ARCHITECTURE.md`, `DATABASE_DESIGN.md`, `API_DOCUMENTATION.md`, `AI_MODEL_DOCUMENTATION.md`, `UI_UX_GUIDE.md`, and `DEVELOPMENT_ROADMAP.md`.
- Modeled the complete system architecture with Mermaid sequence and component diagrams.

### AI Engine (`ai_engine/`)
- Built OpenCV `ImageQualityGatekeeper` with Laplacian focus variance detection, luminance histogram bounds, and HSV/YCrCb skin-presence verification.
- Developed PyTorch `DermaVisionClassifier` utilizing MobileNetV3-Large with custom 3-class classifier head and Temperature Scaling post-processing.
- Implemented `GradCAM` class with forward/backward hook registration, ReLU thresholding, jet colormap application, and alpha blending.
- Implemented `DermaVisionPipeline` orchestrating validation -> preprocessing -> inference -> Grad-CAM -> clinical triage advice.

### Backend (`backend/`)
- Implemented FastAPI application with versioned `/api/v1` routers.
- Designed SQLAlchemy models (`User`, `Analysis`) with cascade deletion.
- Implemented JWT authentication (bcrypt hashing) alongside an instant Guest Demo Mode.
- Created `StorageService` managing isolated directories for raw captures, heatmaps, and blended overlays.
- Implemented full analysis lifecycle: `POST /analysis/process`, `GET /analysis/history`, and `DELETE /analysis/{id}`.
- Added educational endpoints serving verified guides on Acne, Eczema, and Dermatological Red Flags.

### Mobile Client (`mobile/`)
- Translated the user-provided "Crextio" reference image into an editorial, anxiety-reducing mobile design system: "Warm Cream, Amber Gold & Charcoal Glass".
- Implemented 12 interactive mobile screens in `mobile/index.html` and `mobile/app.js`:
  - Splash, Onboarding Carousel, Login/Guest, Home Dashboard, Camera Viewfinder, Review & Crop, Loading, Results, History, Educational Hub, Profile, and Settings.
  - Built an interactive **Grad-CAM Dual-View Comparison Slider** allowing real-time dragging between original photo and AI attention heatmap.
- Created React Native Expo component scaffold (`mobile/App.tsx`) with design tokens and API services.

### Bug Fixes & Deep In-Depth Validations
- Fixed quality gate execution sequence so luminance/exposure verification precedes blur check, preventing black/white captures from being misdiagnosed as blur.
- Resolved Python package naming constraint by renaming `ai-engine` to `ai_engine`.
- Replaced threaded `aiosqlite` with robust standard SQLAlchemy session management to eliminate SQLite thread-locking on Windows with Python 3.13.
- All 12 automated unit and integration tests passing (`12 passed in 13.09s`).
