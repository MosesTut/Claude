from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.itinerary import Itinerary
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.utils.auth import get_current_user

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def submit_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit feedback/report for an AI-generated itinerary

    CRITICAL: This is a REQUIRED feature for AI apps per Apple Guideline 5.1.1.
    The FeedbackScreen MUST be accessible from every itinerary.

    Feedback Types:
    - "inaccurate": Factual errors, wrong information
    - "inappropriate": Offensive or unsuitable content
    - "missing_information": Important details missing
    - "other": General feedback

    Compliance Team Review:
    - "inappropriate" or "inaccurate" reports trigger Slack alerts
    - All reports reviewed within 48 hours
    """

    # Verify itinerary exists and belongs to user
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == feedback_data.itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Itinerary not found or access denied"
        )

    # Validate feedback type
    valid_types = ["inaccurate", "inappropriate", "missing_information", "other"]
    if feedback_data.feedback_type not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid feedback type. Must be one of: {', '.join(valid_types)}"
        )

    # Create feedback record
    new_feedback = Feedback(
        user_id=current_user.id,
        itinerary_id=feedback_data.itinerary_id,
        feedback_type=feedback_data.feedback_type,
        comments=feedback_data.comments,
        reviewed="pending"
    )

    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    # TODO: Send Slack alert for inappropriate/inaccurate reports
    if feedback_data.feedback_type in ["inappropriate", "inaccurate"]:
        # In production, send Slack webhook to #compliance-alerts channel
        print(f"⚠️ COMPLIANCE ALERT: {feedback_data.feedback_type} report for itinerary {feedback_data.itinerary_id}")

    return FeedbackResponse.from_orm(new_feedback)
