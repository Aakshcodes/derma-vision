# DermaVision AI — REST API Documentation (v1)

**Base URL:** `https://api.dermavision.ai/api/v1` (Production) / `http://localhost:8000/api/v1` (Development)  
**Authentication Scheme:** `Bearer <JWT_ACCESS_TOKEN>`

---

## 1. Authentication & User Management

### 1.1 `POST /auth/register`
Creates a standard user account.
- **Request Body (`application/json`):**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!",
    "display_name": "Jordan Doe"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "user": {
      "id": "7b8e1f54-d8bc-4679-b3b3-8f0a1c1d09e1",
      "email": "user@example.com",
      "display_name": "Jordan Doe",
      "is_anonymous": false
    },
    "tokens": {
      "access_token": "eyJhbGciOi...",
      "refresh_token": "d98f7e2a...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
  ```

### 1.2 `POST /auth/login`
Authenticates an existing user via credentials.
- **Request Body (`application/json`):**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }
  ```
- **Response (200 OK):** User object and JWT tokens.

### 1.3 `POST /auth/guest`
Initializes a temporary anonymous session for frictionless MVP evaluation.
- **Response (201 Created):**
  ```json
  {
    "user": {
      "id": "e3a8904f-1244-4f2a-8869-2f5a8991a0b3",
      "is_anonymous": true
    },
    "tokens": {
      "access_token": "eyJhbGciOi...",
      "token_type": "bearer",
      "expires_in": 86400
    }
  }
  ```

### 1.4 `DELETE /users/me`
Permanently deletes the authenticated user, all linked scan records, and all stored imagery.
- **Headers:** `Authorization: Bearer <token>`
- **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "User account and all associated clinical scans have been permanently deleted."
  }
  ```

---

## 2. Image Quality Gate & AI Analysis

### 2.1 `POST /analysis/process`
Primary multimodal endpoint: receives skin photograph, executes quality filter, runs CNN inference, computes temperature-calibrated probabilities, and generates Grad-CAM overlays.

- **Headers:** `Authorization: Bearer <token>`
- **Request Body (`multipart/form-data`):**
  - `file`: Binary image file (`image/jpeg`, `image/png`)
  - `anatomical_site`: Optional string (e.g., `"Forearm"`, `"Face"`, `"Back"`)
- **Successful Response (200 OK):**
  ```json
  {
    "id": "a90184c2-9e88-4fb7-8c34-71239ab7cd89",
    "status": "COMPLETED",
    "prediction": {
      "category": "Acne",
      "confidence": 0.942,
      "calibrated_probabilities": {
        "Acne": 0.942,
        "Eczema": 0.041,
        "Normal": 0.017
      },
      "uncertainty_score": 0.12,
      "is_inconclusive": false
    },
    "visualizations": {
      "original_image_url": "/api/v1/media/orig/a90184c2.jpg",
      "heatmap_overlay_url": "/api/v1/media/overlay/a90184c2.jpg",
      "explanation_note": "Visual attention focused heavily on localized follicular erythematous papules."
    },
    "clinical_guidance": {
      "triage_level": "MILD_SELF_CARE",
      "summary": "Visual features strongly resemble inflammatory acne vulgaris.",
      "recommendations": [
        "Cleanse skin with gentle non-comedogenic cleanser.",
        "Avoid picking or manual lesion extraction to prevent scarring.",
        "Consult a certified dermatologist if inflammatory lesions persist beyond 4 weeks."
      ],
      "dermatologist_consult_advised": false
    },
    "model_metadata": {
      "architecture": "MobileNetV3-Large",
      "version": "1.0.0",
      "device": "cpu"
    },
    "created_at": "2026-11-16T02:00:00Z"
  }
  ```

- **Quality Failure Response (422 Unprocessable Entity):**
  ```json
  {
    "error_code": "QUALITY_CHECK_FAILED",
    "message": "Image quality insufficient for accurate AI evaluation.",
    "reasons": [
      {
        "criterion": "BLUR_DETECTION",
        "value": 42.1,
        "threshold": 85.0,
        "actionable_advice": "Camera movement detected. Please steady your hands against a surface and retake."
      }
    ]
  }
  ```

### 2.2 `GET /analysis/{analysis_id}`
Retrieves a specific prior analysis with refreshed presigned media URLs.

### 2.3 `GET /analysis/history`
Returns paginated list of user's past scans.
- **Query Parameters:** `page=1&limit=20`
- **Response (200 OK):**
  ```json
  {
    "items": [
      {
        "id": "a90184c2-9e88-4fb7-8c34-71239ab7cd89",
        "category": "Acne",
        "confidence": 0.942,
        "thumbnail_url": "/api/v1/media/thumb/a90184c2.jpg",
        "anatomical_site": "Face",
        "created_at": "2026-11-16T02:00:00Z"
      }
    ],
    "total": 1,
    "page": 1,
    "pages": 1
  }
  ```

### 2.4 `DELETE /analysis/{analysis_id}`
Deletes a specific historical scan and its associated media files.

---

## 3. Educational Knowledge Hub

### 3.1 `GET /education/articles`
Returns verified skin health articles, categorized by Acne, Eczema, Sun Care, and Myths.

### 3.2 `GET /education/articles/{slug}`
Returns full medical article markdown, peer-reviewed clinical citations, and triage guidelines.

---

## 4. System Health & Observability

### 4.1 `GET /health`
Returns operational status of the API, Database connection, and Model weights readiness.
- **Response (200 OK):**
  ```json
  {
    "status": "healthy",
    "database": "connected",
    "model_loaded": true,
    "model_version": "mobilenet_v3_large_v1.0.0",
    "timestamp": "2026-11-16T02:00:00Z"
  }
  ```
