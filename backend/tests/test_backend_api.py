"""
Backend API & Service Integration Tests for DermaVision AI
Directly tests API endpoints, authentication flows, analysis pipeline, and database persistence.
Avoids Windows/Python 3.13 anyio threadlock issues.
"""

import io
import cv2
import numpy as np
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.core.database import Base
from backend.app.core.security import decode_access_token
from backend.app.models.entities import User, Analysis
from backend.app.schemas.auth import UserLogin, UserRegister
from backend.app.main import health_check
from backend.app.api.v1.auth import register, login, create_guest_session, get_current_user
import asyncio
from backend.app.api.v1.education import list_articles, get_article
from backend.app.services.analysis_service import analysis_service

# Test SQLite in-memory database
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=test_engine)
    session = TestSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=test_engine)


def create_test_image_bytes(is_blurry: bool = False) -> bytes:
    img = np.zeros((300, 300, 3), dtype=np.uint8)
    img[:, :] = [140, 160, 220]  # Skin tone in BGR
    cv2.circle(img, (150, 150), 30, (40, 50, 190), -1)  # Simulated lesion
    noise = np.random.normal(0, 8, (300, 300, 3)).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    if is_blurry:
        img = cv2.GaussianBlur(img, (31, 31), 0)

    success, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()


def test_health_check():
    data = health_check()
    assert data["status"] == "healthy"
    assert "DermaVision" in data["service"]
    assert data["model_architecture"] == "MobileNetV3-Large"
    assert data["explainability"] == "Grad-CAM Enabled"


def test_auth_registration_and_login(db):
    # 1. Register
    reg_payload = UserRegister(
        email="testuser@dermavision.ai",
        password="StrongPassword123!",
        display_name="Test User",
    )
    res_reg = register(data=reg_payload, db=db)
    assert res_reg["user"].email == "testuser@dermavision.ai"
    assert "access_token" in res_reg["tokens"]
    token = res_reg["tokens"]["access_token"]

    # 2. Get Me (Authenticated)
    me = get_current_user(token=token, db=db)
    assert me.email == "testuser@dermavision.ai"
    assert me.display_name == "Test User"

    # 3. Login
    login_payload = UserLogin(
        email="testuser@dermavision.ai",
        password="StrongPassword123!",
    )
    res_login = login(data=login_payload, db=db)
    assert "access_token" in res_login["tokens"]


def test_guest_session(db):
    res = create_guest_session(db=db)
    assert res["user"].is_anonymous is True
    assert "access_token" in res["tokens"]


def test_analysis_pipeline_end_to_end(db):
    # 1. Create a guest user for the scan
    guest_res = create_guest_session(db=db)
    user_id = guest_res["user"].id

    # 2. Test quality rejection on blurry image
    blurry_bytes = create_test_image_bytes(is_blurry=True)
    success, fail_payload = analysis_service.analyze_and_store(
        db=db,
        user_id=user_id,
        image_bytes=blurry_bytes,
        anatomical_site="Forearm",
    )
    assert success is False
    assert fail_payload["status"] == "FAILED_QUALITY"
    assert fail_payload["error_code"] == "IMAGE_TOO_BLURRY"

    # 3. Test successful analysis on sharp image
    valid_bytes = create_test_image_bytes(is_blurry=False)
    success_valid, result = analysis_service.analyze_and_store(
        db=db,
        user_id=user_id,
        image_bytes=valid_bytes,
        anatomical_site="Forearm",
    )
    assert success_valid is True
    assert result["status"] == "COMPLETED"
    assert "prediction" in result
    assert "visualizations" in result
    assert "clinical_guidance" in result

    analysis_id = result["id"]

    # 4. Test history retrieval
    history_items = analysis_service.get_user_history(db=db, user_id=user_id)
    assert len(history_items) == 1
    assert history_items[0]["id"] == analysis_id
    assert history_items[0]["anatomical_site"] == "Forearm"

    # 5. Test delete
    deleted = analysis_service.delete_analysis(db=db, user_id=user_id, analysis_id=analysis_id)
    assert deleted is True

    # 6. Verify deleted from history
    history_after = analysis_service.get_user_history(db=db, user_id=user_id)
    assert len(history_after) == 0


def test_education_endpoints():
    articles = list_articles()
    assert len(articles) >= 3

    slug = articles[0]["slug"]
    single = get_article(slug=slug)
    assert single["slug"] == slug
    assert single["category"] is not None
