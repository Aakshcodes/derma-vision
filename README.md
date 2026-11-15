# DermaVision AI

> **Accessible, Explainable AI-Powered Skin Health Awareness**  
> *Mobile-First • PyTorch MobileNetV3 • Calibrated Softmax • Grad-CAM Visual Heatmaps • FastAPI & SQLite/PostgreSQL*

---

## 🌟 Overview & Product Philosophy

DermaVision AI is a mobile-first application designed to help users identify potential skin concerns through smartphone photographs, explainable AI visual heatmaps (Grad-CAM), and verified educational guidance.

> **CRITICAL MEDICAL DISCLAIMER:**  
> DermaVision AI is strictly an **educational awareness and triage screening tool**. It does **NOT** provide a definitive medical diagnosis, prescribe pharmaceutical treatment, or replace a certified dermatologist.

---

## 🎨 Visual Design System: Warm Cream, Amber Gold & Charcoal

Inspired by clean, human-centered dashboard design, DermaVision AI rejects cold, sterile clinical blues in favor of warm, anxiety-reducing palettes:
- **Canvas Base:** `#FAF7EE` (Warm Butter Ivory) with soft champagne ambient glows (`#FEF5D7`).
- **High-Contrast Elements:** `#181818` (Charcoal Obsidian) for structured data containers and pill buttons.
- **Affirmative Accent:** `#F6CF4E` (Warm Amber Gold) for confidence meters and active controls.
- **Curvature:** `rounded-3xl` (24–28px) cards and full pill capsules (`rounded-full`).

---

## 🚀 Key Features

1. **Pre-Inference Quality Gatekeeper:** Automatic OpenCV-based filters rejecting blurry ($Var < 75$), underexposed, or non-skin captures before neural inference.
2. **Calibrated MobileNetV3 Classifier:** 3-class classification (Acne, Eczema, Normal skin) with post-hoc Temperature Scaling and Shannon Entropy uncertainty rejection.
3. **Explainable AI (Grad-CAM):** Forward and backward hook-driven class activation maps rendered side-by-side with original photos via an interactive dual-view slider.
4. **Frictionless Authentication:** JWT-based email/password registration alongside an instant **Guest Demo Mode**.
5. **Privacy & Right to be Forgotten:** One-click hard account deletion with automatic cascade deletion of all database records and storage images.
6. **12 Comprehensive Mobile Screens:**
   - Splash Screen
   - Onboarding Carousel (3 Slides)
   - Authentication & Guest Mode
   - Home Dashboard ("Welcome in, Jordan")
   - Camera Viewfinder & Optical HUD
   - Image Review & Quality Preview
   - Multi-Stage Analysis Loading
   - Analysis Results with Interactive Grad-CAM Slider
   - Scan History Timeline & Single/All Deletion
   - Educational Knowledge Hub & Article Reader
   - User Profile & Privacy Controls
   - Settings & Mandatory Medical Disclosures

---

## 🛠️ Monorepo Architecture

```
dermavision-ai/
├── ai_engine/               # Core Computer Vision & Deep Learning Engine
│   ├── explainability/      # Grad-CAM implementation & Colormap Blending
│   ├── inference/           # End-to-end analysis pipeline
│   ├── models/              # MobileNetV3-Large & Calibrated Softmax
│   ├── preprocessing/       # Quality Gatekeeper (Blur, Exposure, Skin Area)
│   └── tests/               # Standalone AI unit test suite
├── backend/                 # FastAPI REST API Engine
│   ├── app/
│   │   ├── api/v1/          # Endpoints (/auth, /analysis, /education)
│   │   ├── core/            # Database engine, Security (JWT/bcrypt), Config
│   │   ├── models/          # SQLAlchemy Entities (User, Analysis)
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   └── services/        # StorageService, AnalysisService
│   ├── tests/               # Backend integration test suite
│   └── main.py              # Application entrypoint
├── mobile/                  # Mobile-First Application
│   ├── index.html           # Standalone Responsive Mobile Web/PWA App
│   ├── app.js               # Mobile State, Interactive Slider, 12 Screens
│   ├── App.tsx              # React Native / Expo application component
│   └── package.json         # Expo dependencies
├── docs/                    # Complete Engineering & Medical Documentation Suite
│   ├── PRD.md               # Product Requirements Document
│   ├── TRD.md               # Technical Requirements Document
│   ├── SYSTEM_ARCHITECTURE.md # System & Component Mermaid Architecture
│   ├── DATABASE_DESIGN.md   # PostgreSQL/SQLite Schema & ER Diagram
│   ├── API_DOCUMENTATION.md # OpenAPI REST Specifications
│   ├── AI_MODEL_DOCUMENTATION.md # Model benchmark & Grad-CAM math
│   ├── UI_UX_GUIDE.md       # Design tokens & screen layouts
│   └── DEVELOPMENT_ROADMAP.md # 7-Phase implementation roadmap
├── storage/                 # Private media storage (Originals, Heatmaps, Overlays)
├── pytest.ini               # Pytest configuration
└── README.md
```

---

## 🧪 Testing & Verification

Run the entire automated test suite (12 tests across AI Engine and Backend):

```powershell
.venv\Scripts\python.exe -m pytest ai_engine/tests backend/tests -v
```

All 12 unit and integration tests verify:
- Blur and low-resolution rejection
- Non-skin exposure failure handling
- High-fidelity synthetic skin acceptance
- Forward pass, calibrated temperature scaling, and entropy calculation
- Grad-CAM heatmap generation and overlay blending
- User registration, login, and JWT issuance
- Guest session generation
- Multipart image analysis and metadata persistence
- History timeline retrieval and hard deletion
- Educational article endpoints

---

## 🏃 Running the Application

### 1. Launch the Backend Server
```powershell
.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
Interactive Swagger Documentation: `http://localhost:8000/docs`

### 2. Launch the Mobile Client
Open [`mobile/index.html`](file:///c:/Users/lenovo/OneDrive/AAKASHCODES/derma%20vision/mobile/index.html) in any browser (or simulate a mobile device using Chrome DevTools `Ctrl+Shift+M`).

