from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.entities import User
from ...schemas.analysis import AnalysisListItem, AnalysisResponse, QualityFailureResponse
from ...services.analysis_service import analysis_service
from .auth import get_current_user

router = APIRouter(prefix="/analysis", tags=["Analysis"])


@router.post(
    "/process",
    response_model=AnalysisResponse,
    responses={422: {"model": QualityFailureResponse}},
)
async def process_skin_image(
    file: UploadFile = File(...),
    anatomical_site: str = Form("Unspecified"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Validate content type
    if file.content_type not in ["image/jpeg", "image/png", "image/webp", "image/jpg"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a JPEG, PNG, or WebP image.",
        )

    # Read bytes
    image_bytes = await file.read()
    if len(image_bytes) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds maximum allowable limit (15 MB).",
        )

    # Execute inference & storage
    success, payload = analysis_service.analyze_and_store(
        db=db,
        user_id=current_user.id,
        image_bytes=image_bytes,
        anatomical_site=anatomical_site,
    )

    if not success:
        # Quality check failure
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=payload,
        )

    return payload


@router.get("/history", response_model=List[AnalysisListItem])
def get_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analysis_service.get_user_history(
        db=db,
        user_id=current_user.id,
        limit=limit,
        offset=offset,
    )


@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis_record(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    deleted = analysis_service.delete_analysis(
        db=db,
        user_id=current_user.id,
        analysis_id=analysis_id,
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis record not found or unauthorized.",
        )
