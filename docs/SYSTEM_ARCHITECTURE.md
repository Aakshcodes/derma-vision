# DermaVision AI — System Architecture Specification

**Version:** 1.0.0  
**Status:** Approved for Implementation

---

## 1. High-Level System Architecture

The following diagram illustrates the relationship between the mobile client, API gateway, backend services, AI inference pipeline, database, and private storage.

```mermaid
flowchart TD
    subgraph Client["Mobile Frontend (React Native + Expo)"]
        UI["UI Components & Navigation"]
        CAM["Camera & Image Picker"]
        CACHE["Zustand Store & TanStack Query"]
    end

    subgraph Gateway["FastAPI Backend (Port 8000)"]
        AUTH["Auth & Rate Limiting Middleware"]
        ROUTER["API Router (/api/v1)"]
        VAL["Image Quality Gatekeeper (OpenCV)"]
    end

    subgraph AI["AI Inference Engine (PyTorch)"]
        PRE["Tensor Preprocessing (224x224)"]
        CNN["CNN Backbone (MobileNetV3 / EfficientNet)"]
        CAL["Calibrated Softmax & Uncertainty"]
        CAM_GEN["Grad-CAM Heatmap Generator"]
    end

    subgraph Persistence["Storage & Data Layer"]
        PG[("PostgreSQL 15+ Database")]
        OBJ[("Private Object / Secure Media Storage")]
    end

    CAM -->|"Raw Skin Capture"| UI
    UI -->|"HTTPS POST /api/v1/analysis/process"| AUTH
    AUTH --> ROUTER
    ROUTER --> VAL
    VAL -->|"Quality Rejection"| UI
    VAL -->|"Quality Validated"| PRE
    PRE --> CNN
    CNN --> CAL
    CNN --> CAM_GEN
    CAL --> ROUTER
    CAM_GEN -->|"Heatmap & Overlay"| ROUTER
    ROUTER -->|"Store Image & Heatmap"| OBJ
    ROUTER -->|"Save Analysis Metadata"| PG
    ROUTER -->|"Return Structured Result JSON"| CACHE
    CACHE --> UI
```

---

## 2. Component Architecture

```mermaid
graph LR
    subgraph MobileLayer["Mobile Layer (TypeScript)"]
        Screens["Screens (12 App Screens)"]
        Components["Atomic Design Elements"]
        Services["Axios API Clients"]
        State["State Stores"]
    end

    subgraph BackendLayer["Backend Layer (FastAPI)"]
        Controllers["Endpoints (/auth, /analysis, /education)"]
        Services_BE["Business Logic Services"]
        Repositories["Async Database Repositories"]
        Schemas["Pydantic Schemas"]
    end

    subgraph EngineLayer["AI Module (PyTorch)"]
        Validator["Quality Filter (Blur/Luminance/Skin)"]
        Classifier["Deep Classifier & Calibration"]
        Explainer["Grad-CAM Extractor"]
    end

    Screens --> Components
    Components --> State
    State --> Services
    Services --> Controllers
    Controllers --> Schemas
    Controllers --> Services_BE
    Services_BE --> Repositories
    Services_BE --> Validator
    Validator --> Classifier
    Classifier --> Explainer
```

---

## 3. Mobile Navigation Flow Diagram

```mermaid
stateDiagram-v2
    [*] --> Splash
    Splash --> Onboarding : First Run
    Splash --> MainTabNavigator : Authenticated / Guest
    Splash --> AuthScreen : Session Expired

    Onboarding --> AuthScreen : Complete Slides
    AuthScreen --> MainTabNavigator : Login / Guest Mode

    state MainTabNavigator {
        [*] --> HomeDashboard
        HomeDashboard --> CameraCapture : "Start Scan" CTA
        HomeDashboard --> EducationHub : "Read Article"
        HomeDashboard --> AnalysisHistory : "View All"
        HomeDashboard --> ProfileScreen : Profile Tab
        
        CameraCapture --> ImagePreview : Capture / Gallery Pick
        ImagePreview --> CameraCapture : Retake
        ImagePreview --> AnalysisLoading : Confirm & Analyze
        
        AnalysisLoading --> AnalysisResult : Success (Inference Done)
        AnalysisLoading --> ImagePreview : Quality Failed (Blur/Lighting)
        
        AnalysisResult --> AnalysisHistory : "Save to History"
        AnalysisResult --> HomeDashboard : Done
        
        AnalysisHistory --> AnalysisResult : Open Past Record
    }
```

---

## 4. AI Inference Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Mobile App
    participant API as FastAPI Router
    participant Gate as Quality Gatekeeper
    participant Torch as PyTorch Model
    participant XAI as Grad-CAM Hook
    participant DB as PostgreSQL
    participant Store as Object Storage

    User->>API: POST /api/v1/analysis/process (multipart image)
    API->>Gate: Validate Resolution, Blur (Laplacian), Exposure, Skin Tone
    alt Image Fails Quality Gate
        Gate-->>API: Quality Exception (e.g. Blurry or No Skin)
        API-->>User: 422 Unprocessable Entity with Guidance Prompt
    else Quality Passed
        Gate->>Torch: Tensor Preprocessing (Resize, Normalize)
        Torch->>Torch: Forward Pass (Feature Maps & Logits)
        Torch->>Torch: Calibrated Softmax ($T$-scaled) & Entropy Check
        Torch->>XAI: Backpropagate Gradients of Predicted Class to Target Conv Layer
        XAI->>XAI: Compute Weighted Activation Map & Overlay (Jet Colormap)
        XAI-->>API: Original Image, Heatmap Image, Overlay Image
        API->>Store: Save Original & Grad-CAM Overlay with SHA256 Key
        API->>DB: Insert Analysis Record (Prediction, Confidence, ABCDE, Timestamps)
        API-->>User: 200 OK (JSON with Prediction, Calibrated Confidence, Signed URLs)
    end
```

---

## 5. Deployment Architecture

```mermaid
flowchart TD
    subgraph ClientDevices["Client Devices"]
        Android["Android Device (APK / AAB)"]
        iOS["iOS Device (TestFlight / IPA)"]
    end

    subgraph Ingress["Ingress / Reverse Proxy"]
        Nginx["Nginx / Caddy (SSL Termination, Rate Limiting)"]
    end

    subgraph AppCluster["Application Container Cluster"]
        FastAPI_1["FastAPI Worker 1 (Uvicorn)"]
        FastAPI_2["FastAPI Worker 2 (Uvicorn)"]
        PyTorch_CPU["PyTorch Inference Module (Shared Weights)"]
    end

    subgraph DataCluster["Data & Persistence Services"]
        PG[("PostgreSQL 15 Container")]
        Volume[("Encrypted Media Volume / S3 Bucket")]
    end

    Android -->|"HTTPS"| Nginx
    iOS -->|"HTTPS"| Nginx
    Nginx --> FastAPI_1
    Nginx --> FastAPI_2
    FastAPI_1 --> PyTorch_CPU
    FastAPI_2 --> PyTorch_CPU
    FastAPI_1 --> PG
    FastAPI_2 --> PG
    FastAPI_1 --> Volume
    FastAPI_2 --> Volume
```
