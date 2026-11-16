from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .api.v1.analysis import router as analysis_router
from .api.v1.auth import router as auth_router
from .api.v1.education import router as education_router
from .core.config import settings
from .core.database import Base, engine

# Ensure tables are created on initialization
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API and AI Inference Service for DermaVision AI",
    version="1.0.0",
)

# CORS middleware for mobile client communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local media storage directory
app.mount("/api/v1/media", StaticFiles(directory=str(settings.STORAGE_DIR)), name="media")

# Register versioned API routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(analysis_router, prefix=settings.API_V1_STR)
app.include_router(education_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "api_version": "v1",
        "database": "connected",
        "model_architecture": "MobileNetV3-Large",
        "explainability": "Grad-CAM Enabled",
    }


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


@app.get("/mobile", include_in_schema=False)
def mobile_redirect():
    return RedirectResponse(url="/")


# Mount the mobile web application at root and /mobile
from pathlib import Path
mobile_dir = Path(__file__).resolve().parent.parent.parent / "mobile"
if mobile_dir.exists():
    app.mount("/mobile", StaticFiles(directory=str(mobile_dir), html=True), name="mobile_frontend_alias")
    app.mount("/", StaticFiles(directory=str(mobile_dir), html=True), name="mobile_frontend")

