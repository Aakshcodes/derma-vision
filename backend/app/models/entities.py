import json
import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from ..core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    display_name = Column(String(100), default="Guest User")
    is_anonymous = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    predicted_category = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)
    is_uncertain = Column(Boolean, default=False)
    status = Column(String(30), default="COMPLETED")
    anatomical_site = Column(String(50), default="Unspecified")

    raw_image_path = Column(String(512), nullable=False)
    heatmap_path = Column(String(512), nullable=True)
    overlay_path = Column(String(512), nullable=True)

    # JSON-encoded metadata
    calibrated_probabilities = Column(Text, default="{}")
    clinical_summary = Column(Text, nullable=True)
    recommendations = Column(Text, default="[]")

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    user = relationship("User", back_populates="analyses")

    def get_probabilities(self) -> dict:
        try:
            return json.loads(self.calibrated_probabilities)
        except Exception:
            return {}

    def get_recommendations(self) -> list:
        try:
            return json.loads(self.recommendations)
        except Exception:
            return []
